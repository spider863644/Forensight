import os
import json
import hashlib
import zipfile
from datetime import datetime
from typing import List, Dict, Optional

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_keys(analyst_name: str, key_dir: str = "keys") -> Dict[str,str]:
    """
    Generate an RSA key pair for the analyst and save to disk.
    Returns dictionary with paths: {'private_key':..., 'public_key':...}
    """
    os.makedirs(key_dir, exist_ok=True)
    private_key_path = os.path.join(key_dir, f"{analyst_name}_private.pem")
    public_key_path = os.path.join(key_dir, f"{analyst_name}_public.pem")

    # Generate RSA key
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # Save private key
    with open(private_key_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Save public key
    public_key = private_key.public_key()
    with open(public_key_path, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    return {"private_key": private_key_path, "public_key": public_key_path}



# --------------------------------------------------------
# Utility functions
# --------------------------------------------------------

def sha256_of(path: str) -> str:
    """Return SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()


def create_output_dir(base_dir: str = "reports") -> str:
    """Create timestamped output directory to avoid overwriting."""
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_dir = os.path.join(base_dir, f"run_{ts}")
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


# --------------------------------------------------------
# Evidence manifest & chain-of-custody
# --------------------------------------------------------

class EvidenceManifest:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.manifest_path = os.path.join(output_dir, "manifest.json")
        self.custody_log_path = os.path.join(output_dir, "chain_of_custody.log")
        self.records: List[Dict] = []
        self._init_log()

    def _init_log(self):
        with open(self.custody_log_path, "a", encoding="utf-8") as f:
            f.write(f"\n--- New session started {datetime.utcnow().isoformat()}Z ---\n")

    def add_evidence(self, file_path: str, analyst: str, description: str = ""):
        record = {
            "file": os.path.basename(file_path),
            "path": os.path.abspath(file_path),
            "sha256": sha256_of(file_path),
            "added_by": analyst,
            "description": description,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        self.records.append(record)
        self._log_action("EVIDENCE_ADDED", record)
        self.save_manifest()

    def _log_action(self, action: str, record: Dict):
        with open(self.custody_log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.utcnow().isoformat()}Z] {action}: {record['file']} by {record['added_by']}\n")

    def log_action(self, action: str, analyst: str, note: str = ""):
        with open(self.custody_log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.utcnow().isoformat()}Z] {action} by {analyst} {note}\n")

    def save_manifest(self):
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=2)


# --------------------------------------------------------
# Digital signing & secure packaging
# --------------------------------------------------------

def sign_file(file_path: str, private_key_path: str) -> str:
    """Digitally sign a file and return signature path."""
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)

    with open(file_path, "rb") as f:
        data = f.read()

    signature = private_key.sign(
        data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    sig_path = file_path + ".sig"
    with open(sig_path, "wb") as f:
        f.write(signature)
    return sig_path


def verify_signature(file_path: str, signature_path: str, public_key_path: str) -> bool:
    """Verify a previously signed file."""
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())

    with open(file_path, "rb") as f:
        data = f.read()
    with open(signature_path, "rb") as f:
        signature = f.read()

    try:
        public_key.verify(
            signature,
            data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False


def package_evidence(output_dir: str, archive_name: Optional[str] = None) -> str:
    """Zip everything in output_dir into a single archive."""
    if not archive_name:
        archive_name = os.path.basename(output_dir.rstrip(os.sep))
    archive_path = os.path.join(os.path.dirname(output_dir), f"{archive_name}.zip")
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(output_dir):
            for f in files:
                path = os.path.join(root, f)
                zf.write(path, os.path.relpath(path, output_dir))
    return archive_path
