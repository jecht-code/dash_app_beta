import pandas as pd

# Create the data with the original entries
data = [
    {
        'Division': 'CPD',
        'Brand': 'Thayers',
        'Category': 'Skin Care',
        'Franchise': 'Body Moisturizer',
        'SubFranchise': 'Body',
        'ParentTag': 'Skin CareBody Moisturizer',
        'Activity': 'Non-Active'
    },
    {
        'Division': 'CPD',
        'Brand': 'Thayers',
        'Category': 'Skin Care',
        'Franchise': 'Body Moisturizer',
        'SubFranchise': 'Body',
        'ParentTag': 'Skin CareBody Moisturizer',
        'Activity': 'Non-Active'
    },
    {
        'Division': 'CPD',
        'Brand': 'Thayers',
        'Category': 'Skin Care',
        'Franchise': 'Body Moisturizer',
        'SubFranchise': 'Body',
        'ParentTag': 'Skin CareBody Moisturizer',
        'Activity': 'Active'
    },
    {
        'Division': 'CPD',
        'Brand': 'John',
        'Category': 'Skin Care',
        'Franchise': 'Body Moisturizer',
        'SubFranchise': 'Body',
        'ParentTag': 'Skin CareBody Moisturizer',
        'Activity': 'Active'
    },
    {
        'Division': 'CPD',
        'Brand': 'Thayers',
        'Category': 'Skin Care',
        'Franchise': 'Body Moisturizer',
        'SubFranchise': 'Body',
        'ParentTag': 'Skin CareBody Moisturizer',
        'Activity': 'Active'
    },
    {
        'Division': 'CPD',
        'Brand': 'Michael',
        'Category': 'Skin Care',
        'Franchise': 'Body Moisturizer',
        'SubFranchise': 'Body',
        'ParentTag': 'Skin CareBody Moisturizer',
        'Activity': 'Active'
    },
    {
        'Division': 'CPD',
        'Brand': 'Thayers',
        'Category': 'Skin Care',
        'Franchise': 'Body Moisturizer',
        'SubFranchise': 'Body',
        'ParentTag': 'Skin CareBody Moisturizer',
        'Activity': 'Active'
    }
]

# Create DataFrame and save to Excel
df = pd.DataFrame(data)
df.to_excel('Catalog_File.xlsx', index=False)
print("Data restored successfully!") 