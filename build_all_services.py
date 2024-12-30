import os
import subprocess

def run_command(command):
    result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
    print(result.stdout)

def main():
    # Build and delete token service repo
    print("Clonando el repositorio del servicio de tokens...")
    run_command("git clone https://github.com/IgnaRoz/apiREST.git token_service_rep")
    os.chdir("token_service_rep")
    print("Instalando dependencias del servicio de tokens...")
    run_command("pip install .")
    print("Construyendo el servicio de tokens...")
    run_command("./build.sh")
    os.chdir("..")
    print("Eliminando el repositorio del servicio de tokens...")
    run_command("rm -rf token_service_rep")
    
    # Build and delete authentication repo
    print("Clonando el repositorio del servicio de autenticación...")
    run_command("git clone --branch entregable2 https://github.com/luideoz/Authentication.git adi_auth_srv_rep")
    os.environ["STORAGE_FOLDER"] = "storage"
    os.chdir("adi_auth_srv_rep")
    print("Instalando dependencias del servicio de autenticación...")
    run_command("pip install .")
    print("Iniciando el servicio de autenticación...")
    run_command("python3 bootstrap.py")
    print("Construyendo el servicio de autenticación...")
    run_command("./build.sh")
    os.chdir("..")
    print("Eliminando el repositorio del servicio de autenticación...")
    run_command("rm -rf adi_auth_srv_rep")
    
    # Build and delete blob service repo
    print("Clonando el repositorio del servicio de blobs...")
    run_command("git clone --branch main https://github.com/SergiooCoorne/Blob_Service_ADI.git blob_service_rep")
    os.chdir("blob_service_rep")
    print("Construyendo el servicio de blobs...")
    run_command("./scripts/build.sh")
    os.chdir("..")
    print("Eliminando el repositorio del servicio de blobs...")
    run_command("rm -rf blob_service_rep")

if __name__ == "__main__":
    main()