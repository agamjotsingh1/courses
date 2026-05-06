import tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

# generate the verilog header (.vh) file
with open("config.vh", "w") as f:
    f.write("// AUTO-GENERATED FILE. DO NOT EDIT DIRECTLY.\n")
    f.write("// Sourced from config.toml\n\n")
    
    for key, value in config.items():
        # Convert keys to uppercase for standard Verilog macro naming
        macro_name = key.upper()
        f.write(f"`define {macro_name} {value}\n")
        
print("Successfully generated config.vh from config.toml")