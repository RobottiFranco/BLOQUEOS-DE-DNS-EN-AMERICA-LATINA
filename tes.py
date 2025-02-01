import csv
import os
import re

def parse_dig_output(dig_file, output_csv):
    results = []
    
    with open(dig_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    domain = None
    resolver = None
    status = None
    
    for line in lines:
        if "<<>> DiG" in line:
            match = re.search(r"<<>> DiG.*?<<>>\s+(\S+)", line)
            if match:
                domain = match.group(1).strip().rstrip(".")
        
        elif "@" in line:
            match = re.search(r"@(\d+\.\d+\.\d+\.\d+)", line)
            if match:
                resolver = match.group(1).strip()

        elif "status:" in line:
            match = re.search(r"status:\s+(\S+)", line)
            if match:
                status = match.group(1).strip()
        
        if domain and resolver and status:
            results.append([domain, resolver, status])
            domain, resolver, status = None, None, None
    
    with open(output_csv, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["dominio", "resolvedor", "status"])
        writer.writerows(results)

    print(f"✅ CSV generado en: {output_csv}")


input_folder = "src/data/digs/resultados"
output_folder = "src/data/digs/toCSV"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.csv")
        print(f"🔄 Procesando {filename}...")
        parse_dig_output(input_path, output_path)