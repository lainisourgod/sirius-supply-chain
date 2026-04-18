import pickletools
import zipfile

with zipfile.ZipFile("sirius_text_embedder/pytorch_model.bin") as zf:
    print("PyTorch Model is ZIP. Files:\n")

    for file in zf.namelist():
        print(file)

    for fname in [
        "pytorch_model/.format_version",
        "pytorch_model/.storage_alignment",
        "pytorch_model/byteorder",
        "pytorch_model/version",
        "pytorch_model/.data/serialization_id",
    ]:
        with zf.open(fname) as f:
            content = f.read()
            print(f"\n--- {fname} ---")
            try:
                # Try to decode as utf-8 for text files
                print(content.decode("utf-8"))
            except Exception:
                print(content)

    print("\nDecompiling data.pkl...\n")

    with zf.open("pytorch_model/data.pkl") as f:
        pickletools.dis(f)
