import os

REPO = input("Enter repo destination: ")
print(f"Animations will be rendered to {REPO}/render/")

os.system(f"cd {REPO}")

for file in os.listdir("src"):
    if file[-3:] == ".py":
        output = (
            f"{REPO}/render/{file[:-3]}.mp4"
        )
        path = f"src/{file}"
        os.system(f"manim -qm -o {output} {path}")

print(f"Animations rendered to {REPO}/render/")
