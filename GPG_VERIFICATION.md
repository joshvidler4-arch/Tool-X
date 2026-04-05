# GPG Signature Verification for Tool-X

## Overview

Tool-X includes an embedded GPG public key to verify the authenticity of the repository and its author. This ensures that users can trust the code they are running.

## Author GPG Key Information

- **Key Type**: RSA-3072
- **Creation Date**: 2026-04-05
- **Fingerprint**: `D09D4264D329A2E56BF74B407A10EA59EC609CF1`
- **Owner**: josh (public key signed welcome) <joshvidler4@gmail.com>

## Quick Verification

To verify the GPG signature embedded in this repository, run:

```bash
python3 verify_gpg.py
```

This will:
1. Extract the embedded GPG public key from `tool-x.py`
2. Import it into your GPG keyring
3. Verify the fingerprint matches the expected value
4. Display key information

## Manual Verification

If you prefer to verify manually:

### Step 1: Extract the Key

The GPG public key is embedded in `tool-x.py` at lines 7-31. You can extract it with:

```bash
python3 -c "
with open('tool-x.py', 'r') as f:
    content = f.read()
    start = content.find('-----BEGIN PGP PUBLIC KEY BLOCK-----')
    end = content.find('-----END PGP PUBLIC KEY BLOCK-----') + len('-----END PGP PUBLIC KEY BLOCK-----')
    print(content[start:end])
" > author_key.asc
```

### Step 2: Import the Key

```bash
gpg --import author_key.asc
```

### Step 3: Verify the Fingerprint

```bash
gpg --fingerprint joshvidler4@gmail.com
```

Expected output should show:
```
pub   rsa3072 2026-04-05 [SC]
      D09D4264D329A2E56BF74B407A10EA59EC609CF1
uid           [ unknown] josh (public key signed welcome) <joshvidler4@gmail.com>
```

### Step 4: Trust the Key (Optional)

If you want to mark this key as trusted in your GPG keyring:

```bash
gpg --edit-key D09D4264D329A2E56BF74B407A10EA59EC609CF1
# In the GPG prompt, type: trust
# Select trust level: 5 (ultimate trust)
# Type: quit
```

## Verifying Signed Commits

If commits in this repository are GPG-signed, you can verify them with:

```bash
# Verify the last commit
git verify-commit HEAD

# Show signature info for the last commit
git log --show-signature -1

# Verify a specific commit
git verify-commit <commit-hash>
```

## Security Best Practices

1. **Always verify the fingerprint**: The fingerprint `D09D4264D329A2E56BF74B407A10EA59EC609CF1` should match exactly
2. **Check the key owner**: Ensure it belongs to `joshvidler4@gmail.com`
3. **Verify signed commits**: Check that important commits are GPG-signed
4. **Keep GPG updated**: Use the latest version of GPG for security patches

## What is GPG Signature Verification?

GPG (GNU Privacy Guard) is a tool for secure communication and data signing. In the context of this repository:

- **Authenticity**: Confirms the code comes from the stated author
- **Integrity**: Ensures the code hasn't been tampered with
- **Non-repudiation**: The author cannot deny having signed the code

## Troubleshooting

### Key Import Fails

If importing the key fails:
1. Ensure GPG is installed: `gpg --version`
2. Check the key file format is correct (ASCII-armored)
3. Try importing with verbose output: `gpg --import --verbose author_key.asc`

### Fingerprint Doesn't Match

If the fingerprint doesn't match:
1. **DO NOT USE THIS REPOSITORY** - it may have been tampered with
2. Report the issue to the repository maintainers
3. Download from the official source

### "Unknown" Trust Level

The `[unknown]` trust level is normal for newly imported keys. You can manually set the trust level if you've verified the key's authenticity through other means.

## Additional Resources

- [GnuPG Documentation](https://gnupg.org/documentation/)
- [GitHub GPG Signature Verification](https://docs.github.com/en/authentication/managing-commit-signature-verification)
- [OpenPGP Best Practices](https://riseup.net/en/security/message-security/openpgp/best-practices)

## Support

For issues related to GPG verification:
- Check existing issues: https://github.com/joshvidler4-arch/Tool-X/issues
- Contact: joshvidler4@gmail.com
