"""
This code is provided under the terms of the GNU General Public License (GPL) as published by
the Free Software Foundation, either version 3 of the License, or any
later version. See <https://www.gnu.org/licenses/>.

Author: [Synthaze (GitHub)](https://github.com/synthaze)
Email: [Dr. Florian Malard (florian.malard@gmail.com), Prof. Dr. Stéphanie Olivier-van Stichelen (solivier@mcw.edu)]
"""
# Import necessary libraries
import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import py4cytoscape as p4c
import requests
import sys

# Create a tkinter application
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Create file selector section
        self.create_file_selector()

        # Create parameters sections for Intracellular and Extracellular
        self.create_parameters('Intracellular', ['cytosol', 'nucleus', 'mitochondrion'], 4)
        self.create_parameters('Extracellular', ['endoplasmic reticulum', 'golgi apparatus', 'plasma membrane', 'extracellular'], 4.4)

        # Create PSM parameter section
        self.create_psm_parameter()

        # Create submit button
        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=15, column=0, columnspan=2, pady=10)

    def create_file_selector(self):
        # Information label for file selection
        self.info_label = tk.Label(self, text='Data file in CSV format such as: "Protein Accessions,HexNAc,PSM"', justify=tk.LEFT)
        self.info_label.grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=10)

        # Button to select a file
        self.file_button = tk.Button(self, text="Select File", command=self.select_file)
        self.file_button.grid(row=1, column=0, sticky='w', padx=10, pady=10)

        # Label to display selected file path
        self.file_label = tk.Label(self, text="No file selected")
        self.file_label.grid(row=1, column=1, sticky='w', padx=10, pady=10)

    def create_parameters(self, category, compartments, default_value):
        # Base row for Intracellular and Extracellular sections
        base_row = {'Intracellular': 2, 'Extracellular': 7}[category]

        # Information label for parameter section
        self.info_label = tk.Label(self, text=f"{category}: enrichment greater than x, with x in [0, 5]", justify=tk.LEFT)
        self.info_label.grid(row=base_row, column=0, columnspan=2, sticky='w', padx=10, pady=10)

        if category == 'Intracellular':
            j = 1
        else:
            j = 4

        for i, compartment in enumerate(compartments):
            # Entry widget for specifying parameter values
            entry = tk.Entry(self)
            entry.grid(row=base_row + i + 1, column=1)
            entry.insert(0, str(default_value))
            setattr(self, f'param{j}_entry', entry)

            # Label to display compartment name
            label = tk.Label(self, text=f"compartment::{compartment}")
            label.grid(row=base_row + i + 1, column=0, sticky='w', padx=10)
            j += 1

    def create_psm_parameter(self):
        # Information label for PSM parameter
        self.info_label = tk.Label(self, text="Top O-GlcNAc targets: PSM greater than x, with x in [0, +inf]", justify=tk.LEFT)
        self.info_label.grid(row=13, column=0, columnspan=2, sticky='w', padx=10, pady=10)

        # Entry widget for PSM threshold
        self.psm_entry = tk.Entry(self)
        self.psm_entry.grid(row=14, column=1)
        self.psm_entry.insert(0, '5')

        # Label for PSM entry
        self.psm_label = tk.Label(self, text="PSM Threshold")
        self.psm_label.grid(row=14, column=0, sticky='w', padx=10)

    def select_file(self):
        # Open a file dialog to select a CSV file
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_label.config(text=file_path)

    def submit(self):
        # Get file path, parameters, and PSM threshold, and load data
        self.dpath = self.file_label.cget("text")
        self.conditions = {
            'Intracellular': {
                'compartment::cytosol': float(self.param1_entry.get()),
                'compartment::nucleus': float(self.param2_entry.get()),
                'compartment::mitochondrion': float(self.param3_entry.get())
            },
            'Extracellular': {
                'compartment::endoplasmic reticulum': float(self.param4_entry.get()),
                'compartment::golgi apparatus': float(self.param5_entry.get()),
                'compartment::plasma membrane': float(self.param6_entry.get()),
                'compartment::extracellular': float(self.param7_entry.get())
            }
        }
        self.cutoff_PSM = float(self.psm_entry.get())
        self.load_data()

    def load_data(self):
        # Destroy existing widgets and load data from CSV
        for ele in self.master.winfo_children():
            ele.destroy()

        self.data = pd.read_csv(self.dpath, sep=',').drop_duplicates()
        self.tree = ttk.Treeview(self.master)
        self.tree["columns"] = list(self.data.columns)
        self.tree["show"] = "headings"

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Insert data into the treeview
        for _, row in self.data.iterrows():
            self.tree.insert("", "end", values=list(row))

        self.tree.pack(expand=True, fill='both')

        validate_button = tk.Button(self.master, text="Validate", command=self.process_cytoscape)
        validate_button.pack(side='left', padx=10, pady=10)

        quit_button = tk.Button(self.master, text="Quit", command=self.master.destroy)
        quit_button.pack(side='right', padx=10, pady=10)

    def stringdb_mapping(self):
        # Perform mapping to STRING database
        string_api_url = 'https://string-db.org/api'
        output_format = 'json'
        method = 'get_string_ids'

        params = {
            'identifiers' : '\r'.join(self.proteins),
            'limit' : 1,
        }

        request_url = '/'.join([string_api_url, output_format, method])
        results = requests.post(request_url, data=params)

        if results.status_code == 200:
            return pd.DataFrame(results.json())
        else:
            raise Exception(f"Error querying STRING database: {results.status_code}")

    def process_cytoscape(self):
        # Rename columns, perform STRING database query, and process data in Cytoscape
        self.data.rename(columns={'Protein Accessions':'queryItem'}, inplace=True)
        self.proteins = self.data['queryItem'].tolist()
        mapping = self.stringdb_mapping()
        data = pd.merge(self.data, mapping).drop(['queryIndex'], axis=1).dropna(axis='columns')
        proteins = data['stringId'].tolist()

        # Perform STRING protein query in Cytoscape
        p4c.cytoscape_ping()
        proteins = ','.join(proteins)
        p4c.commands.commands_post(f'string protein query query={proteins} limit=0')
        edges = p4c.get_all_edges()
        p4c.hide_edges(edges)

        # Retrieve and clean table
        nodes = p4c.get_table_columns()

        # Merge with data
        data.rename(columns={'stringId': 'name'}, inplace=True)
        nodes = pd.merge(nodes, data, on='name', how='inner')

        # Compute properties based on parameters
        nodes['Intracellular'] = nodes.apply(lambda row: any(row[col] > threshold for col, threshold in self.conditions['Intracellular'].items()), axis=1)
        nodes['Extracellular'] = nodes.apply(lambda row: any(row[col] > threshold for col, threshold in self.conditions['Extracellular'].items()), axis=1)

        nodes['O-GlcNAc probability'] = 'Unknownn HexNAc'

        nodes.loc[nodes['HexNAc'] == 0, 'O-GlcNAc probability'] = 'No HexNAc'
        nodes.loc[(nodes['HexNAc'] > 0) & (nodes['Extracellular'] == 1), 'O-GlcNAc probability'] = 'Extracellular HexNAc'
        nodes.loc[(nodes['HexNAc'] > 0) & (nodes['Intracellular'] == 1), 'O-GlcNAc probability'] = 'O-GlcNAcylated proteins'
        nodes.loc[(nodes['HexNAc'] > 0) & (nodes['Intracellular'] == 1) & (nodes['PSM'] > self.cutoff_PSM), 'O-GlcNAc probability'] = 'Top O-GlcNAc Targets'

        p4c.load_table_data(nodes, data_key_column='name', table='node', table_key_column='name')

        for col in ['stringdb::full name', 'stringdb::database identifier', '@id', 'preferredName', 'annotation', 'queryItem', 'query term', 'stringdb::STRING style', 'stringdb::enhancedLabel Passthrough', 'stringdb::namespace', 'ncbiTaxonid', 'taxonName']:
            p4c.delete_table_column(col)

        # Set Cytoscape style
        p4c.commands.commands_post('layout attributes-layout nodeAttribute="O-GlcNAc probability"')
        style_name = p4c.import_visual_styles('style.xml')[0]
        p4c.set_visual_style(style_name)

        p4c.commands.commands_post('autoannotate annotate-clusterBoosted useClusterMaker=false clusterIdColumn="O-GlcNAc probability" labelColumn="O-GlcNAc probability"')

        sys.exit()

# Create the main tkinter window
root = tk.Tk()
root.title('Cytovs - v0.1')

# Create the application instance
app = Application(master=root)
app.pack()

# Start the tkinter main loop
root.mainloop()
