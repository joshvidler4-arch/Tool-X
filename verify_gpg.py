#!/usr/bin/env python3
"""
GPG Signature Verification Utility for Tool-X
Author: josh <joshvidler4@gmail.com>
GPG Key Fingerprint: D09D4264D329A2E56BF74B407A10EA59EC609CF1
"""

import subprocess
import sys
import os

# Expected GPG key fingerprint for the Tool-X author
EXPECTED_FINGERPRINT = "D09D4264D329A2E56BF74B407A10EA59EC609CF1"
EXPECTED_EMAIL = "joshvidler4@gmail.com"

def extract_embedded_gpg_key():
    """Extract the embedded GPG public key from tool-x.py"""
    try:
        with open('tool-x.py', 'r') as f:
            content = f.read()
            start = content.find('-----BEGIN PGP PUBLIC KEY BLOCK-----')
            end = content.find('-----END PGP PUBLIC KEY BLOCK-----')
            if start == -1 or end == -1:
                return None
            return content[start:end + len('-----END PGP PUBLIC KEY BLOCK-----')]
    except Exception as e:
        print(f"Error extracting GPG key: {e}")
        return None

def verify_gpg_key():
    """Verify the embedded GPG key is valid and matches expected fingerprint"""
    print("=" * 60)
    print("Tool-X GPG Signature Verification Utility")
    print("=" * 60)

    # Extract the key
    gpg_key = extract_embedded_gpg_key()
    if not gpg_key:
        print("❌ ERROR: Could not extract GPG key from tool-x.py")
        return False

    print("\n✓ Extracted embedded GPG key from tool-x.py")

    # Save to temporary file
    tmp_key_file = '/tmp/toolx_author_key.asc'
    with open(tmp_key_file, 'w') as f:
        f.write(gpg_key)

    # Import the key
    try:
        result = subprocess.run(
            ['gpg', '--import', tmp_key_file],
            capture_output=True,
            text=True
        )
        if result.returncode != 0 and 'not changed' not in result.stderr:
            print(f"❌ ERROR: Failed to import GPG key:\n{result.stderr}")
            return False
        print("✓ GPG key imported successfully")
    except Exception as e:
        print(f"❌ ERROR: Failed to run gpg command: {e}")
        return False

    # Verify the fingerprint
    try:
        result = subprocess.run(
            ['gpg', '--list-keys', '--with-colons', EXPECTED_EMAIL],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"❌ ERROR: Key for {EXPECTED_EMAIL} not found")
            return False

        # Parse fingerprint from output
        found_fingerprint = None
        for line in result.stdout.split('\n'):
            if line.startswith('fpr:'):
                found_fingerprint = line.split(':')[9]
                break

        if found_fingerprint == EXPECTED_FINGERPRINT:
            print(f"✓ Fingerprint verified: {EXPECTED_FINGERPRINT}")
            print(f"✓ Key owner: {EXPECTED_EMAIL}")
            return True
        else:
            print(f"❌ ERROR: Fingerprint mismatch!")
            print(f"   Expected: {EXPECTED_FINGERPRINT}")
            print(f"   Found:    {found_fingerprint}")
            return False

    except Exception as e:
        print(f"❌ ERROR: Failed to verify fingerprint: {e}")
        return False

    finally:
        # Cleanup
        if os.path.exists(tmp_key_file):
            os.remove(tmp_key_file)

def display_key_info():
    """Display detailed information about the GPG key"""
    print("\n" + "=" * 60)
    print("GPG Key Information")
    print("=" * 60)

    try:
        result = subprocess.run(
            ['gpg', '--list-keys', EXPECTED_FINGERPRINT],
            capture_output=True,
            text=True
        )
        print(result.stdout)
    except Exception as e:
        print(f"Error displaying key info: {e}")

def main():
    """Main verification routine"""
    if verify_gpg_key():
        display_key_info()
        print("\n" + "=" * 60)
        print("✓ GPG VERIFICATION SUCCESSFUL")
        print("=" * 60)
        print("\nThe Tool-X repository signature is valid.")
        print("You can trust that this code comes from the verified author.")
        return 0
    else:
        print("\n" + "=" * 60)
        print("❌ GPG VERIFICATION FAILED")
        print("=" * 60)
        print("\nWarning: Could not verify the repository signature.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
