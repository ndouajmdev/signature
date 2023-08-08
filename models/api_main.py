from odoo import _, api, fields, models, tools

from odoo.exceptions import UserError
from werkzeug.utils import secure_filename
import requests
import json
import base64
import os


class Api_modele(models.Model):
    _name = 'api.modele'
    _description = 'Api model'
    
    
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user)
    data_field = fields.Html(string="Data Field", readonly=True)
    name_field = fields.Html(string="name Field", readonly=True)
    id_user = fields.Char(string="Id", readonly=True)
    recipient_email = fields.Char(string="Email")
    
    doc = fields.Binary(string='Fichier', required=True)
    
    fichier_id = fields.One2many(
        'field.model',
        'api_ids',
        string='Fichier charger',
        )
    
    nom_du_fichier = fields.Char( related='fichier_id.name',string="Nom du fichier")
   
   
   
    # etape 2
    
    
    etape_two = fields.Html(string="Etape 2", readonly=True)
    workflow_id = fields.Char( string="Workflow Id", readonly=True)
    
    
    # etape 3
    etape_tree = fields.Html(string="Etape 3", readonly=True)
    
    # etape 4
    etape_four = fields.Html(string="Etape 4", readonly=True)
    hash = fields.Char(string="Hash", readonly=True)
    size = fields.Char(string="Size", readonly=True)
    
    # etape 5
    etape_five = fields.Html(string="Etape 5", readonly=True)
    
    # etape 6
    etap_six = fields.Html(string="Etape 6", readonly=True)
    
    def get_user_data(self):

        url = "https://wm-test01.artci-sign.ci/api/users"
        headers = {
            'Authorization': 'Bearer act_BGwL8QuvQppCoXhzf92ummK6.2v2XwsXaSXTh8fzW4GoFL5pMqJxdirAq9LUJAyRAeRhaDUDdGnZJc97hUY9gvJqM'
        }
        params = {
            'items.email': 'yassi.michael@artci.ci'
        }
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        self.data_field = data  # Mettre à jour la valeur du champ 'data_field' avec les données récupérées de l'API
        
        # Extraire le champ 'lastName' des données récupérées
        # last_name = data['items'][0]['lastName']
        
        id = data['items'][0]['id']
  

        # self.name_field = last_name  # Mettre à jour la valeur du champ 'data_field' avec le champ 'lastName'
        self.id_user = id
        return data
    
    
    def action_two(self):
        self.ensure_one()

        url_two = f"https://wm-test01.artci-sign.ci/api/users/{self.id_user}/workflows/"

        payload = json.dumps({
        "name": "TestMicen",
        "steps": [
            {
            "stepType": "signature",
            "recipients": [
                {
                "consentPageId": "cop_BgKmiR1nxZEeBiGtYhswaUUc",
                "userId": self.id_user
                }
            ],
            "sendDownloadLink": False,
            "hideWorkflowRecipients": True
            }
        ]
        })
        headers = {
        'Authorization': 'Bearer act_BGwL8QuvQppCoXhzf92ummK6.2v2XwsXaSXTh8fzW4GoFL5pMqJxdirAq9LUJAyRAeRhaDUDdGnZJc97hUY9gvJqM',
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url_two, headers=headers, data=payload)
        data_two = response.json()
        self.etape_two = data_two
        
        id = data_two['id']
        self.workflow_id = id
        
        return data_two



    def action_tree(self):
        self.ensure_one()
        url = f"https://wm-test01.artci-sign.ci/api/workflows/{self.workflow_id}/parts"
      # Récupérer le contenu du champ doc
      
        file_content = self.doc

        # Encoder le contenu en base64 et le convertir en chaîne de caractères
        document_content = base64.b64encode(file_content).decode('utf-8')

        payload = {
            "doc": document_content
        }

        headers = {
            'Authorization': 'Bearer act_BGwL8QuvQppCoXhzf92ummK6.2v2XwsXaSXTh8fzW4GoFL5pMqJxdirAq9LUJAyRAeRhaDUDdGnZJc97hUY9gvJqM',
            'Content-Type': 'application/json'
        }

        headers = {
            'Authorization': 'Bearer act_BGwL8QuvQppCoXhzf92ummK6.2v2XwsXaSXTh8fzW4GoFL5pMqJxdirAq9LUJAyRAeRhaDUDdGnZJc97hUY9gvJqM',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload)
        data_tree = response.json()
        self.etape_tree = data_tree
        
        code_hash = data_tree['parts'][0]['hash']
        code_size = data_tree['parts'][0]['size']
        
        self.hash = code_hash
        self.size = code_size
        return data_tree

   


    def action_four(self):
        self.ensure_one()
        
        url_four = f"https://wm-test01.artci-sign.ci/api/workflows/{self.workflow_id}/documents"

        payload = json.dumps({
        "parts": [
            {
            "filename": "Document",
            "contentType": "application/pdf",
            "size": self.size,
            "hash": self.hash
            }
        ],
        "signatureProfileId": "sip_KA49jsZB5kMY82cGACwYgwp8",
        "pdfSignatureFields": [
            {
            "imagePage": -1,
            "imageX": 390,
            "imageY": 710,
            "imageWidth": 150,
            "imageHeight": 80
            }
        ]
        })
        headers = {
        'Authorization': 'Bearer act_BGwL8QuvQppCoXhzf92ummK6.2v2XwsXaSXTh8fzW4GoFL5pMqJxdirAq9LUJAyRAeRhaDUDdGnZJc97hUY9gvJqM',
        'Content-Type': 'application/json',
        'Content-Length': '383'
        }

        response = requests.request("POST", url_four, headers=headers, data=payload)
        data_four = response.json()
        self.etape_four = data_four
        
        return data_four
 

    def action_five(self):
        self.ensure_one()

        url = f"https://wm-test01.artci-sign.ci/api/workflows/{self.workflow_id}"

        payload = {
            "workflowStatus": "started"
        }
        headers = {
            'Authorization': 'Bearer act_BGwL8QuvQppCoXhzf92ummK6.2v2XwsXaSXTh8fzW4GoFL5pMqJxdirAq9LUJAyRAeRhaDUDdGnZJc97hUY9gvJqM',
            'Content-Type': 'application/json',
        }

        response = requests.request("PATCH", url, headers=headers, json=payload)
        data_five = response.json()
        self.etape_five = data_five
        
        # Ouvrir le pop-up avec les données
        return data_five


    def action_six(self):
        self.ensure_one()

        url = f"https://wm-test01.artci-sign.ci/api/workflows/{self.workflow_id}/invite"

        payload = json.dumps({
        "recipientEmail": "yassi.michael@artci.ci"
        })
        headers = {
        'Authorization': 'Bearer act_BGwL8QuvQppCoXhzf92ummK6.2v2XwsXaSXTh8fzW4GoFL5pMqJxdirAq9LUJAyRAeRhaDUDdGnZJc97hUY9gvJqM',
        'Content-Type': 'application/json',
        'Content-Length': '48'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        data_six = response.json()
        self.etap_six = data_six
        return data_six


    def execute_all_actions(self):
        self.ensure_one()
        
        # Étape 1 : Récupérer les données de l'utilisateur
        self.get_user_data()
        
        # Étape 2 : Exécuter l'action two
        self.action_two()
        
        # Étape 3 : Exécuter l'action tree
        self.action_tree()
        
        # Étape 4 : Exécuter l'action four
        self.action_four()
        
        # Étape 5 : Exécuter l'action five
        self.action_five()
        
        # Étape 6 : Exécuter l'action six
        self.action_six()

        # Vous pouvez également effectuer d'autres opérations ici si nécessaire
        
        # Retourner les données finales si nécessaire
        return {
            'data_field': self.data_field,
            'etape_two': self.etape_two,
            'etape_tree': self.etape_tree,
            'etape_four': self.etape_four,
            'etape_five': self.etape_five,
            'etap_six': self.etap_six
        }


class File_model(models.Model):

    _name = 'field.model'
    _description = 'Fichier Joint'
    
    
    name = fields.Char()
    nom_fichier = fields.Char()
    
    document = fields.Binary()
    
    api_ids = fields.Many2one('api.modele')

    @api.onchange('nom_fichier')
    def _onchange_file_name(self):
        if self.nom_fichier and not self.name:
            self.name = self.nom_fichier
            
            
            
            
            
            
            

# def action_tree(self):
#     self.ensure_one()
#     url = f"https://wm-test01.artci-sign.ci/api/workflows/{self.workflow_id}/parts"

#     # Récupérer le contenu du champ doc
#     file_content = self.doc

#     # Encoder le contenu en base64 et le convertir en chaîne de caractères
#     document_content = base64.b64encode(file_content).decode('utf-8')

#     payload = {
#         "doc": document_content
#     }

#     headers = {
#         'Authorization': 'Bearer act_BGwL8QuvQppCoXhzf92ummK6.2v2XwsXaSXTh8fzW4GoFL5pMqJxdirAq9LUJAyRAeRhaDUDdGnZJc97hUY9gvJqM',
#         'Content-Type': 'application/json'
#     }

#     response = requests.post(url, headers=headers, json=payload)
#     data_tree = response.json()
#     self.etape_tree = data_tree

#     code_hash = data_tree['parts'][0]['hash']
#     code_size = data_tree['parts'][0]['size']

#     self.hash = code_hash
#     self.size = code_size
#     return data_tree

# def action_five(self):
    #     self.ensure_one()

    #     url = f"https://wm-test01.artci-sign.ci/api/workflows/{self.workflow_id}"

    #     payload = json.dumps({
    #     "workflowStatus": "started"
    #     })
    #     headers = {
    #     'Authorization': 'Bearer act_BGwL8QuvQppCoXhzf92ummK6.2v2XwsXaSXTh8fzW4GoFL5pMqJxdirAq9LUJAyRAeRhaDUDdGnZJc97hUY9gvJqM',
    #     'Content-Type': 'application/json',
    #     'Content-Length': '1183'
    #     }

    #     response = requests.request("PATCH", url, headers=headers, data=payload)
    #     data_five = response.json()
    #     self.etape_five = data_five
    #     return data_five