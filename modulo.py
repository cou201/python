import os
import csv
import matplotlib.pyplot as plt

def read_csv(file_path):
    """
    Reads a CSV file and returns the data as a list of dictionaries.
    """
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def create_folders_and_files(materials, projects):
    """
    Creates folders for each material and writes material reports into text files.
    """
    if not os.path.exists("Materials report"):
        os.mkdir("Materials report")
    
    for material in materials:
        material_name = material["Nombre"]  # Using "Nombre" as per original
        material_id = material["ID"]
        unit_value = float(material["Valor Unitario"])  # Using "Valor Unitario"
        
        # Create a folder for each material
        folder_path = os.path.join("Materials report", material_name)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        
        # Calculate totals and averages
        total_quantity = 0
        total_cost = 0
        count = 0
        for project in projects:
            if project["ID Material"] == material_id:
                quantity = int(project["Cantidad"])  # Using "Cantidad"
                total_quantity += quantity
                total_cost += quantity * unit_value
                count += 1
        
        average = total_quantity / count if count > 0 else 0
        
        # Write to a text file
        file_path = os.path.join(folder_path, f"{material_name}.txt")
        with open(file_path, 'w') as file:
            file.write(f"Total quantity of material: {total_quantity}\n")
            file.write(f"Average material used: {average:.2f}\n")
            file.write(f"Total material cost: {total_cost:.2f}\n")

def create_graph_folder():
    """
    Creates a folder for saving graph reports.
    """
    if not os.path.exists("Graph reports"):
        os.mkdir("Graph reports")

def plot_bar_chart():
    """
    Creates a bar chart showing the quantity of material used by category and saves it as a .png file.
    """
    categories = {}
    for material in materials:
        category = material["Categoria"]  # Using "Categoria"
        material_id = material["ID"]
        if category not in categories:
            categories[category] = 0
        for project in projects:
            if project["ID Material"] == material_id:
                categories[category] += int(project["Cantidad"])
    
    # Create a bar chart
    plt.figure()
    plt.bar(categories.keys(), categories.values(), color='blue')
    plt.title("Material Quantity by Category")
    plt.xlabel("Categories")
    plt.ylabel("Quantity")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the chart
    file_path = os.path.join("Graph reports", "Material_Quantity_by_Category.png")
    plt.savefig(file_path)
    plt.close()

def plot_pie_chart():
    """
    Creates a pie chart showing project participation by city and saves it as a .png file.
    """
    cities = {}
    for project in projects:
        client_id = project["ID Client"]  # Using "ID Client"
        city = clients_dict.get(client_id, {}).get("Ciudad", "Unknown")  # Using "Ciudad"
        if city not in cities:
            cities[city] = 0
        cities[city] += 1
    
    # Imprimir el contenido del diccionario cities para verificación
    print("Contenido de 'cities':", cities)
    
    # Create a pie chart
    plt.figure()
    plt.pie(cities.values(), labels=cities.keys(), autopct="%1.1f%%", startangle=140)
    plt.title("Project Participation by City")
    plt.tight_layout()
    
    # Save the chart
    file_path = os.path.join("Graph reports", "Project_Participation_by_City.png")
    plt.savefig(file_path)
    plt.close()

def show_graph_menu():
    """
    Displays the menu for creating graphs and executes the selected option.
    """
    print("\nWould you like to create a graphical report?")
    response = input("Type 'yes' or 'no': ").strip().lower()
    
    if response in ["yes"]:
        print("\nChoose the type of graph:")
        print("1. Bar Chart")
        print("2. Pie Chart")
        
        option = input("Enter the number of your choice: ").strip()
        create_graph_folder()
        if option == "1":
            plot_bar_chart()
            print("Bar chart saved successfully.")
        elif option == "2":
            plot_pie_chart()
            print("Pie chart saved successfully.")
        else:
            print("Invalid option. No graph will be created.")
    elif response == "no":
        print("No graph will be created.")
    else:
        print("Invalid response. Please try again.")
        show_graph_menu()


# Load data
clients = read_csv(r"C:\Users\Valeria\OneDrive\Desktop\miniproyectofinal\clientes\Clientes.csv")
materials = read_csv(r"C:\Users\Valeria\OneDrive\Desktop\miniproyectofinal\materiales\Materiales.csv")
projects = read_csv(r"C:\Users\Valeria\OneDrive\Desktop\miniproyectofinal\proyectos\Proyectos.csv")

# Print keys of dictionaries for verification
print("Keys in Clients.csv:", clients[0].keys())
print("Keys in Materials.csv:", materials[0].keys())
print("Keys in Projects.csv:", projects[0].keys())

# Create dictionaries for quick access
clients_dict = {client["Id"]: client for client in clients}
materials_dict = {material["ID"]: material for material in materials}

# Execute main functions
create_folders_and_files(materials, projects)
show_graph_menu()
