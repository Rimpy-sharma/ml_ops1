"""
pdf_to_md.py

Simple converter: extracts text and images from a PDF and writes a Markdown file.
Uses PyMuPDF (a.k.a. fitz).

Usage:
  python pdf_to_md.py "C:\\path\\to\\file.pdf" "C:\\path\\to\\output.md" --images-dir "C:\\path\\to\\images"

If output path is omitted, creates `<input>.md` next to the PDF.
"""
import os
import argparse
import fitz  # PyMuPDF


def pdf_to_markdown(pdf_path: str, md_path: str, images_dir: str = None):
    os.makedirs(os.path.dirname(md_path) or ".", exist_ok=True)
    if images_dir:
        os.makedirs(images_dir, exist_ok=True)

    doc = fitz.open(pdf_path)

    with open(md_path, "w", encoding="utf-8") as md:
        md.write(f"# Converted from `{os.path.basename(pdf_path)}`\n\n")
        md.write(f"_Pages: {len(doc)}_\n\n")

        for i, page in enumerate(doc, start=1):
            text = page.get_text("text")
            md.write(f"## Page {i}\n\n")

            if text:
                # Normalize CRLF and trim trailing spaces
                lines = [ln.rstrip() for ln in text.splitlines()]
                # Join with single newlines so Markdown keeps paragraphs
                md.write("\n".join(lines))
                md.write("\n\n")
            else:
                md.write("*(no extractable text on this page)*\n\n")

            if images_dir:
                image_list = page.get_images(full=True)
                if image_list:
                    md.write(f"### Images on page {i}\n\n")
                for img_index, img in enumerate(image_list, start=1):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image.get("ext", "png")
                    image_filename = f"page{i}_img{img_index}.{image_ext}"
                    image_path = os.path.join(images_dir, image_filename)
                    with open(image_path, "wb") as imf:
                        imf.write(image_bytes)

                    # Use forward slashes in Markdown paths for compatibility
                    rel_path = os.path.join(os.path.basename(images_dir), image_filename).replace('\\\\', '/')
                    md.write(f"![{image_filename}]({rel_path})\n\n")

    doc.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert PDF to Markdown (text + images)")
    parser.add_argument("pdf", help="Input PDF file path")
    parser.add_argument("output", nargs="?", help="Output Markdown file path (optional)")
    parser.add_argument("--images-dir", dest="images_dir", help="Directory to write extracted images (optional)")

    args = parser.parse_args()

    pdf_path = args.pdf
    if not os.path.isfile(pdf_path):
        print(f"ERROR: Input PDF not found: {pdf_path}")
        raise SystemExit(2)

    if args.output:
        md_path = args.output
    else:
        base = os.path.splitext(pdf_path)[0]
        md_path = base + ".md"

    images_dir = args.images_dir
    if images_dir is None:
        # default images dir next to md file
        images_dir = os.path.splitext(md_path)[0] + "_images"

    pdf_to_markdown(pdf_path, md_path, images_dir)
    print(f"Wrote Markdown to: {md_path}")
    print(f"Extracted images into: {images_dir} (if any)")
