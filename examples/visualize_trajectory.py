from ase.io import read, write

from io import StringIO
from PIL import Image
import os
import argparse


# Function to extract a specific frame from the .xyz file
def extract_frame(lines, frame_number):
    # Parse the file
    num_atoms = int(lines[0].strip())  # Number of atoms from the first line
    # print(f"Number of frames: {len(lines) // (num_atoms + 2)}")
    frame_start = frame_number * (num_atoms + 2)  # Start of the desired frame
    frame_lines = lines[frame_start : frame_start + num_atoms + 2]  # Extract frame
    return "".join(frame_lines)


# Function to visualize the trajectory
def visualize_trajectory(xyz_file, reaction_name):
    # Extract the specific frame from the .xyz file

    with open(xyz_file, "r") as f:
        lines = f.readlines()
    num_atoms = int(lines[0].strip())
    num_frames = len(lines) // (num_atoms + 2)

    png_files = []
    for i in range(num_frames):
        frame_data = extract_frame(lines, i)
        file_wrapper = StringIO(frame_data)

        atoms = read(file_wrapper, format="xyz")

        del atoms[
            [atom.index for atom in atoms if atom.index not in [327, 1154, 546, 547]]
        ]

        # Create an ASE view
        f_name = f"reaction_images/{reaction_name}_{i:03}.png"
        write(f_name, atoms, format="png")
        png_files.append(f_name)
    return png_files


def create_gif(png_files, gif_name="output.gif", duration=200):
    """
    Create a GIF from a list of PNG files.

    Args:
        png_files (list): List of PNG file paths.
        gif_name (str): Name of the output GIF file.
        duration (int, optional): Duration of each frame in milliseconds. Defaults to 200.
    """
    images = []
    for png_file in png_files:
        img = Image.open(png_file)
        images.append(img)

    if images:
        images[0].save(
            gif_name,
            save_all=True,
            append_images=images[1:],
            duration=duration,
            loop=0,
            disposal=2,
        )
        print(f"GIF created: {gif_name}")
    else:
        print("No PNG images found in the folder.")


# examples/output/.xyz
def main(reaction_name):
    # Path to the .xyz file
    xyz_file = f"output/{reaction_name}.xyz"

    # Visualize the trajectory
    png_files = visualize_trajectory(xyz_file, reaction_name)
    # Create a GIF from the PNG files
    create_gif(png_files, gif_name=f"output/{reaction_name}.gif", duration=200)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize trajectory and create GIF.")
    parser.add_argument(
        "reaction_name", type=str, help="Name of the reaction to visualize."
    )
    args = parser.parse_args()
    reaction_name = args.reaction_name

    assert os.path.exists(
        f"output/{reaction_name}.xyz"
    ), f"File output/{reaction_name}.xyz does not exist."
    main(reaction_name)
