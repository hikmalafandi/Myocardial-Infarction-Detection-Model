import nbformat

def split_notebook_by_heading(input_nb):
    with open(input_nb, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    sections = []
    current_section = []
    current_title = "part_0"
    data_preparation_cells = []

    for cell in nb.cells:
        if cell.cell_type == "markdown" and cell.source.startswith("# "):  # Heading level 1
            if "data preparation" in cell.source.lower():
                data_preparation_cells.append(cell)  # Simpan bagian Data Preparation
            else:
                if current_section:
                    sections.append((current_title, current_section))
                current_title = cell.source.strip("# ").strip().replace(" ", "_").lower()
                current_section = [cell]
        else:
            if "data preparation" in current_title:
                data_preparation_cells.append(cell)  # Simpan semua sel dalam Data Preparation
            else:
                current_section.append(cell)

    if current_section:
        sections.append((current_title, current_section))

    for i, (title, cells) in enumerate(sections):
        new_nb = nbformat.v4.new_notebook()
        new_nb.cells = data_preparation_cells + cells  # Tambahkan Data Preparation ke setiap file

        output_filename = f"{i+1:02d}_{title}.ipynb"
        with open(output_filename, "w", encoding="utf-8") as out:
            nbformat.write(new_nb, out)
        
        print(f"Saved: {output_filename}")

# Jalankan fungsi ini dengan nama file notebook-mu
split_notebook_by_heading("Klasifikasi_MI.ipynb")
