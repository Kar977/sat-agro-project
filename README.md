1. clone repo $ git clone git@github.com:Kar977/sat-agro-project.git
2. procced the migratoins to the db
3. fetch warnings from IMGW $ python manage.py sync_warning
4. download data from https://mapy.geoportal.gov.pl/ WFS service 'Państwowy Rejestr Granic - Jednostki Terytorialne', choose object 'A02_Granice_powiatow'. Save data for specific county and run command $ python manage.py import_county path/to/file.gml --teryt 'teryt_nbr' --name "County Name"
5. Send the request to get the warnings 'GET /warnings/by_location/?lat=51.532&lon=17.271'
