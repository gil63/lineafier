import os
import subprocess
import lineafier


if __name__ == "__main__":
    for file in os.listdir("./tests"):
        try:
            out1 = subprocess.run(["py", "./tests/" + file], capture_output=True).stdout
            out2 = subprocess.run(["py", "-c", lineafier.convert_file("./tests/" + file)], capture_output=True).stdout
            if out1 == out2:
                print(f"{file} passed")
            else:
                print(f"{file} failed with output {out2}")
        except Exception as e:
            print(f"{file} failed with error: '{e}'")
