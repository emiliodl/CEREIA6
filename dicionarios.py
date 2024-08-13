equivalencia_estadiamento = {
    '' :['[]'],
    'I': ['I', 'IA', 'IB', 'IC'],
    'II': ['II', 'IIA', 'IIB', 'IIC'],
    'III': ['III', 'IIIA', 'IIIB', 'IIIC'],
    'IV': ['IV', 'IVA', 'IVB', 'IVC'],
    'T': ['Tx', 'T0', 'Ta', 'Tis', 'Tis(DCIS)', 'Tis(LAMN)', 'Tis(Paget)', 'T1', 'T1mi', 'T1a', 'T1a1', 'T1a2', 'T1b', 'T1b1', 'T1b2', 'T1b3', 'T1c', 'T1c1', 'T1c2', 'T1c3', 'T1d', 'T2', 'T2a', 'T2a1', 'T2a2', 'T2b', 'T2c', 'T2d', 'T3', 'T3a', 'T3b', 'T3c', 'T3d', 'T3e', 'T4', 'T4a', 'T4b', 'T4c', 'T4d', 'T4e'],
    'N': ['Nx', 'N0', 'N0(sn)', 'N0a', 'N0a(sn)', 'N0b', 'N0b(sn)', 'N0(i+)', 'N0(mol+)', 'N1', 'N1(sn)', 'N1mi', 'N1mi(sn)', 'N1a', 'N1a(sn)', 'N1b', 'N1b(sn)', 'N1c', 'N1c(sn)', 'N2', 'N2mi', 'N2a', 'N2b', 'N2c', 'N3', 'N3a', 'N3b', 'N3c'],
    'M': ['Mx', 'M0', 'M0(i+)', 'M1', 'M1a', 'M1a(0)', 'M1a(1)', 'M1b', 'M1b(0)', 'M1b(1)', 'M1c', 'M1c(0)', 'M1c(1)', 'M1d', 'M1d(0)', 'M1d(1)'],
    'ypT': ['ypT2-4a'],
    'ypN': ['ypN+'],
    'pT': ['pT2-4a'],
    'pN': ['pN+']
}

biomarcadores_dict = {
    'Adenocarcinoma':['HER','PD-L1'], 
    'Anus Neoplasms':['X'], 
    'Anxiety Disorders':['X'], 
    'Biliary Tract Neoplasms':['X'], 
    'Breast Neoplasms':['Ki-67' ,'EGFR','ALK','BRCA1', 'BRCA2','HER','PD-L1','Progesterone','Estrogen'], 
    'Cancer Pain':['X'], 
    'Carcinoma':['MSI','BRAF','EGFR','ALK','ROS1','PD-L1'], 
    'Carcinoma, Merkel Cell':['PD-L1'], 
    'Carcinoma, Non-Small-Cell Lung':['BRAF','KRAS','EGFR','ALK','ROS1','HER','PD-L1'], 
    'Carcinoma, Squamous Cell':['PD-L1'], 
    'Cardiotoxicity':['X'], 
    'Cardiovascular Diseases':['X'], 
    'Cholangiocarcinoma':['X'], 
    'Colonic Neoplasms':['X'], 
    'Colorectal Neoplasms':['MSI','HER'], 
    'Endometrial Neoplasms':['X'], 
    'Epilepsy':['X'], 
    'Epstein-Barr Virus Infections':['X'], 
    'Esophageal Neoplasms':['PD-L1'], 
    'Esophageal Squamous Cell Carcinoma':['BRAF','EGFR','ALK','ROS1','PD-L1'], 
    'Gastrointestinal Stromal Tumors':['X'], 
    'Glioblastoma':['BRAF'], 
    'Head and Neck Neoplasms':['EGFR'], 
    'Hemangioma':['X'], 
    'Hematologic Neoplasms':['X'], 
    'Infections':['X'], 
    'Kidney Neoplasms':['X'], 
    'Leukemia':['EGFR'], 
    'Lung Neoplasms': ['BRAF','KRAS','EGFR','ALK','ROS1','HER','PD-L1'], 
    'Lymphoma':['EGFR','PD-L1'], 
    'Melanoma':['BRAF','ALK','PD-L1'], 
    'Mesothelioma':['X'], 
    'Mouth Neoplasms':['X'], 
    'Mucositis':['X'], 
    'Multiple Myeloma':['EGFR','PD-L1'], 
    'Myasthenia Gravis':['X'], 
    'Neoplasm Metastasis':['X'], 
    'Neoplasms':['Ki-67','MSI','BRAF','EGFR','ALK','ROS1','HER','PD-L1'], 
    'Osteosarcoma':['X'], 
    'Papillomavirus Infections':['X'], 
    'Polycythemia Vera':['X'], 
    'Postoperative Complications':['X'], 
    'Preleukemia':['X'], 
    'Primary Myelofibrosis':['X'], 
    'Primary Ovarian Insufficiency':['X'], 
    'Prostatic Neoplasms':['EGFR','ALK','Estrogen'], 
    'Rectal Neoplasms':['X'], 
    'Sarcoma':['X'], 
    'Sarcoma, Kaposi':['X'], 
    'Squamous Cell Carcinoma of Head and Neck':['MSI','BRAF','EGFR','PD-L1'], 
    'Stomach Neoplasms':['HER'], 
    'Thromboembolism':['X'], 
    'Thyroid Diseases':['X'], 
    'Thyroid Neoplasms':['BRAF','EGFR'], 
    'Thyroid Nodule':['X'], 
    'Urinary Bladder Neoplasms':['PD-L1'], 
    'Uterine Cervical Neoplasms':['ALK','PD-L1'], 
    'Ventricular Dysfunction':['HER'], 
    'Virus Diseases':['X']

}

mesh_dict = {'Lung Neoplasms': ['Carcinoma, Non-Small-Cell Lung'],
             'Biliary Tract Neoplasms': [],
             'Esophageal Neoplasms': ['Esophageal Squamous Cell Carcinoma'], 
             'Lymphoma': ['Lymphoma, Non-Hodgkin', 'Lymphoma, B-Cell'], 
             'Neoplasms': [], 
             'Breast Neoplasms': [], 
             'Carcinoma': ['Carcinoma, Squamous Cell', 'Squamous Cell Carcinoma of Head and Neck'], 
             'Anxiety Disorders': [], 
             'Primary Ovarian Insufficiency': ['Menopause, Premature'], 
             'Neoplasm Metastasis': ['Sarcoma'], 
             'Leukemia': ['Leukemia, Lymphoid', 'Leukemia, Lymphocytic, Chronic, B-Cell'], 
             'Carcinoma, Squamous Cell': ['Squamous Cell Carcinoma of Head and Neck', 'Head and Neck Neoplasms'], 
             'Multiple Myeloma': ['Neoplasms, Plasma Cell'], 
             'Carcinoma, Non-Small-Cell Lung': [], 
             'Melanoma': [],
             'Uterine Cervical Neoplasms': [], 
             'Urinary Bladder Neoplasms': ['Non-Muscle Invasive Bladder Neoplasms'], 
             'Prostatic Neoplasms': ['Hypersensitivity'], 
             'Sarcoma, Kaposi': ['Sarcoma'], 
             'Adenocarcinoma': ['Stomach Neoplasms'], 
             'Head and Neck Neoplasms': [], 
             'Carcinoma, Merkel Cell': ['Carcinoma'], 
             'Preleukemia': ['Anemia', 'Myelodysplastic Syndromes', 'Syndrome'], 
             'Endometrial Neoplasms': [], 
             'Cholangiocarcinoma': [], 
             'Thromboembolism': ['Venous Thromboembolism'], 
             'Polycythemia Vera': ['Primary Myelofibrosis', 'Polycythemia', 'Thrombocytosis', 'Thrombocythemia, Essential'], 
             'Colorectal Neoplasms': [], 
             'Papillomavirus Infections': ['Uterine Cervical Neoplasms'], 
             'Mucositis': ['Xerostomia'], 
             'Sarcoma': [], 
             'Infections': ['Communicable Diseases', 'Papillomavirus Infections', 'Squamous Cell Carcinoma of Head and Neck'], 
             'Hematologic Neoplasms': ['Graft vs Host Disease'], 
             'Osteosarcoma': ['Mucositis', 'Stomatitis'], 
             'Virus Diseases': ['Neoplasms', 'Hematologic Neoplasms', 'Graft vs Host Disease'], 
             'Stomach Neoplasms': [], 
             'Glioblastoma': [], 
             'Thyroid Diseases': [], 
             'Thyroid Nodule': ['Thyroid Diseases'], 
             'Myasthenia Gravis': ['Muscle Weakness'], 
             'Epstein-Barr Virus Infections': ['Lymphoma', 'Lymphoproliferative Disorders'], 
             'Mouth Neoplasms': ['Head and Neck Neoplasms', 'Mucositis', 'Stomatitis'], 
             'Cardiovascular Diseases': ['Cardiotoxicity'], 
             'Mesothelioma': ['Mesothelioma, Malignant'], 
             'Epilepsy': [], 
             'Esophageal Squamous Cell Carcinoma': [], 
             'Anus Neoplasms': [], 
             'Cardiotoxicity': [], 
             'Colonic Neoplasms': ['Thrombosis', 'Venous Thrombosis'], 
             'Thyroid Neoplasms': ['Thyroid Diseases'], 
             'Postoperative Complications': ['Postoperative Nausea and Vomiting'], 
             'Kidney Neoplasms': ['Carcinoma, Renal Cell'], 
             'Ventricular Dysfunction': ['Ventricular Dysfunction, Left'], 
             'Primary Myelofibrosis': [], 
             'Hemangioma': ['Arteriovenous Malformations', 'Congenital Abnormalities'], 
             'Cancer Pain': [], 
             'Squamous Cell Carcinoma of Head and Neck': [], 
             'Rectal Neoplasms': [], 
             'Gastrointestinal Stromal Tumors': []}

opcoes_biomarcadores = {
    'HER': ['positivo', 'negativo', 'neutro'],
    'Estrogen': ['positivo', 'negativo'],
    'Progesterone': ['positivo', 'negativo'],
    'KRAS': ['mutado', 'não-mutado'],
    'PD-L1': ['positivo', 'negativo'],
    'MSI': ['alto', 'baixo'],
    'ALK': ['mutado', 'não-mutado'],
    'BRCA1': ['mutado', 'não-mutado'],
    'BRCA2': ['mutado', 'não-mutado'],
    'BRAF': ['mutado', 'não-mutado'],
    'ROS1': ['mutado', 'não-mutado'],
    'Ki-67': [''],
    'EGFR': ['mutado', 'não-mutado'],
}

bio_to_column = {
    'HER': 'Tipo_Her',
    'Estrogen': 'tipo_estrogen',
    'Progesterone': 'tipo_progesterone',
    'KRAS': 'BiomarkKRAS',
    'PD-L1': 'Tipo_PD_L1',
    'MSI': 'Tipo_MSI',
    'ALK': 'Tipo_ALK',
    'BRAF': 'Tipo_BRAF',
    'ROS1': 'Tipo_ROS1',
    'BRCA1': 'Tipo_BRCA1_BRCA2',
    'BRCA2': 'Tipo_BRCA1_BRCA2', 
    'Ki-67': 'Tipo_de_resultado_Ki67',
    'EGFR': 'Tipo_EGFR'
}