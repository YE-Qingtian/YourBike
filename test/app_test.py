import unittest
from app import app
from unittest.mock import patch
import pandas as pd
from config import GoogleMap_api_key
import json


class TestWeatherApp(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True

    def test_root_endpoint(self):
        # Test the root endpoint that it returns the index page
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # Check if Google Map API key is in the rendered HTML
        self.assertIn(GoogleMap_api_key, response.data.decode())

    @patch('pandas.read_sql_query')
    def test_stations_endpoint(self, mock_read_sql):
        # Mock the pandas read_sql_query function for the stations endpoint
        stations_df = """
        {"0":{"number":"1","contract_name":"dublin","name":"CLARENDON ROW","address":"Clarendon Row","position_lat":53.340927,"position_lng":-6.262501,"banking":0,"bonus":0,"bike_stands":31,"status":"OPEN","last_update":1713391437000,"available_bike_stands":31,"available_bikes":0},"1":{"number":"10","contract_name":"dublin","name":"DAME STREET","address":"Dame Street","position_lat":53.344007,"position_lng":-6.266802,"banking":1,"bonus":0,"bike_stands":16,"status":"OPEN","last_update":1713391560000,"available_bike_stands":3,"available_bikes":13},"2":{"number":"100","contract_name":"dublin","name":"HEUSTON BRIDGE (SOUTH)","address":"Heuston Bridge (South)","position_lat":53.347106,"position_lng":-6.292041,"banking":0,"bonus":0,"bike_stands":25,"status":"OPEN","last_update":1713391677000,"available_bike_stands":2,"available_bikes":23},"3":{"number":"101","contract_name":"dublin","name":"KING STREET NORTH","address":"King Street North","position_lat":53.350291,"position_lng":-6.273507,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391649000,"available_bike_stands":20,"available_bikes":10},"4":{"number":"102","contract_name":"dublin","name":"WESTERN WAY","address":"Western Way","position_lat":53.354929,"position_lng":-6.269425,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391549000,"available_bike_stands":23,"available_bikes":17},"5":{"number":"103","contract_name":"dublin","name":"GRANGEGORMAN LOWER (SOUTH)","address":"Grangegorman Lower (South)","position_lat":53.354663,"position_lng":-6.278681,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391627000,"available_bike_stands":35,"available_bikes":5},"6":{"number":"104","contract_name":"dublin","name":"GRANGEGORMAN LOWER (CENTRAL)","address":"Grangegorman Lower (Central)","position_lat":53.355173,"position_lng":-6.278424,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391660000,"available_bike_stands":31,"available_bikes":9},"7":{"number":"105","contract_name":"dublin","name":"GRANGEGORMAN LOWER (NORTH)","address":"Grangegorman Lower (North)","position_lat":53.355954,"position_lng":-6.278378,"banking":0,"bonus":0,"bike_stands":36,"status":"OPEN","last_update":1713391414000,"available_bike_stands":31,"available_bikes":5},"8":{"number":"106","contract_name":"dublin","name":"RATHDOWN ROAD","address":"Rathdown Road","position_lat":53.35893,"position_lng":-6.280337,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391626000,"available_bike_stands":20,"available_bikes":20},"9":{"number":"107","contract_name":"dublin","name":"CHARLEVILLE ROAD","address":"Charleville Road","position_lat":53.359157,"position_lng":-6.281866,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391428000,"available_bike_stands":21,"available_bikes":19},"10":{"number":"108","contract_name":"dublin","name":"AVONDALE ROAD","address":"Avondale Road","position_lat":53.359405,"position_lng":-6.276142,"banking":0,"bonus":0,"bike_stands":35,"status":"OPEN","last_update":1713391740000,"available_bike_stands":8,"available_bikes":27},"11":{"number":"109","contract_name":"dublin","name":"BUCKINGHAM STREET LOWER","address":"Buckingham Street Lower","position_lat":53.353331,"position_lng":-6.249319,"banking":0,"bonus":0,"bike_stands":29,"status":"OPEN","last_update":1713391594000,"available_bike_stands":23,"available_bikes":6},"12":{"number":"11","contract_name":"dublin","name":"EARLSFORT TERRACE","address":"Earlsfort Terrace","position_lat":53.334295,"position_lng":-6.258503,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391416000,"available_bike_stands":27,"available_bikes":3},"13":{"number":"110","contract_name":"dublin","name":"PHIBSBOROUGH ROAD","address":"Phibsborough Road","position_lat":53.356307,"position_lng":-6.273717,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391428000,"available_bike_stands":33,"available_bikes":7},"14":{"number":"111","contract_name":"dublin","name":"MOUNTJOY SQUARE EAST","address":"Mountjoy Square East","position_lat":53.356717,"position_lng":-6.256359,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391582000,"available_bike_stands":32,"available_bikes":8},"15":{"number":"112","contract_name":"dublin","name":"NORTH CIRCULAR ROAD (O'CONNELL'S)","address":"North Circular Road (O'Connell's)","position_lat":53.357841,"position_lng":-6.251557,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391430000,"available_bike_stands":22,"available_bikes":8},"16":{"number":"113","contract_name":"dublin","name":"MERRION SQUARE SOUTH","address":"Merrion Square South","position_lat":53.338614,"position_lng":-6.248606,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391634000,"available_bike_stands":25,"available_bikes":15},"17":{"number":"114","contract_name":"dublin","name":"WILTON TERRACE (PARK)","address":"Wilton Terrace (Park)","position_lat":53.333653,"position_lng":-6.248345,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391403000,"available_bike_stands":40,"available_bikes":0},"18":{"number":"115","contract_name":"dublin","name":"KILLARNEY STREET","address":"Killarney Street","position_lat":53.354845,"position_lng":-6.247579,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391652000,"available_bike_stands":5,"available_bikes":25},"19":{"number":"116","contract_name":"dublin","name":"BROADSTONE","address":"Broadstone","position_lat":53.3547,"position_lng":-6.272314,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391596000,"available_bike_stands":30,"available_bikes":0},"20":{"number":"117","contract_name":"dublin","name":"HANOVER QUAY EAST","address":"Hanover Quay East","position_lat":53.343653,"position_lng":-6.231755,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391406000,"available_bike_stands":39,"available_bikes":1},"21":{"number":"12","contract_name":"dublin","name":"ECCLES STREET","address":"Eccles Street","position_lat":53.359246,"position_lng":-6.269779,"banking":0,"bonus":0,"bike_stands":20,"status":"OPEN","last_update":1713391608000,"available_bike_stands":18,"available_bikes":2},"22":{"number":"13","contract_name":"dublin","name":"FITZWILLIAM SQUARE WEST","address":"Fitzwilliam Square West","position_lat":53.336074,"position_lng":-6.252825,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391626000,"available_bike_stands":30,"available_bikes":0},"23":{"number":"14","contract_name":"dublin","name":"FOWNES STREET UPPER","address":"Fownes Street Upper","position_lat":53.344603,"position_lng":-6.263371,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391416000,"available_bike_stands":11,"available_bikes":19},"24":{"number":"15","contract_name":"dublin","name":"HARDWICKE STREET","address":"Hardwicke Street","position_lat":53.355473,"position_lng":-6.264423,"banking":0,"bonus":0,"bike_stands":16,"status":"OPEN","last_update":1713391423000,"available_bike_stands":7,"available_bikes":9},"25":{"number":"16","contract_name":"dublin","name":"GEORGES QUAY","address":"Georges Quay","position_lat":53.347508,"position_lng":-6.252192,"banking":0,"bonus":0,"bike_stands":20,"status":"OPEN","last_update":1713391671000,"available_bike_stands":10,"available_bikes":10},"26":{"number":"17","contract_name":"dublin","name":"GOLDEN LANE","address":"Golden Lane","position_lat":53.340803,"position_lng":-6.267732,"banking":0,"bonus":0,"bike_stands":20,"status":"OPEN","last_update":1713391631000,"available_bike_stands":20,"available_bikes":0},"27":{"number":"18","contract_name":"dublin","name":"GRANTHAM STREET","address":"Grantham Street","position_lat":53.334123,"position_lng":-6.265436,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391585000,"available_bike_stands":15,"available_bikes":15},"28":{"number":"19","contract_name":"dublin","name":"HERBERT PLACE","address":"Herbert Place","position_lat":53.334432,"position_lng":-6.245575,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391653000,"available_bike_stands":29,"available_bikes":1},"29":{"number":"2","contract_name":"dublin","name":"BLESSINGTON STREET","address":"Blessington Street","position_lat":53.356769,"position_lng":-6.26814,"banking":0,"bonus":0,"bike_stands":20,"status":"OPEN","last_update":1713391662000,"available_bike_stands":15,"available_bikes":5},"30":{"number":"20","contract_name":"dublin","name":"JAMES STREET EAST","address":"James Street East","position_lat":53.336597,"position_lng":-6.248109,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391410000,"available_bike_stands":30,"available_bikes":0},"31":{"number":"21","contract_name":"dublin","name":"LEINSTER STREET SOUTH","address":"Leinster Street South","position_lat":53.34218,"position_lng":-6.254485,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391432000,"available_bike_stands":30,"available_bikes":0},"32":{"number":"22","contract_name":"dublin","name":"TOWNSEND STREET","address":"Townsend Street","position_lat":53.345922,"position_lng":-6.254614,"banking":0,"bonus":0,"bike_stands":20,"status":"OPEN","last_update":1713391407000,"available_bike_stands":19,"available_bikes":1},"33":{"number":"23","contract_name":"dublin","name":"CUSTOM HOUSE","address":"Custom House","position_lat":53.348279,"position_lng":-6.254662,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391409000,"available_bike_stands":1,"available_bikes":29},"34":{"number":"24","contract_name":"dublin","name":"CATHAL BRUGHA STREET","address":"Cathal Brugha Street","position_lat":53.352149,"position_lng":-6.260533,"banking":0,"bonus":0,"bike_stands":20,"status":"OPEN","last_update":1713391411000,"available_bike_stands":18,"available_bikes":2},"35":{"number":"25","contract_name":"dublin","name":"MERRION SQUARE EAST","address":"Merrion Square East","position_lat":53.339434,"position_lng":-6.246548,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391449000,"available_bike_stands":26,"available_bikes":4},"36":{"number":"26","contract_name":"dublin","name":"MERRION SQUARE WEST","address":"Merrion Square West","position_lat":53.339764,"position_lng":-6.251988,"banking":1,"bonus":0,"bike_stands":20,"status":"OPEN","last_update":1713391431000,"available_bike_stands":20,"available_bikes":0},"37":{"number":"27","contract_name":"dublin","name":"MOLESWORTH STREET","address":"Molesworth Street","position_lat":53.341288,"position_lng":-6.258117,"banking":0,"bonus":0,"bike_stands":20,"status":"OPEN","last_update":1713391424000,"available_bike_stands":20,"available_bikes":0},"38":{"number":"28","contract_name":"dublin","name":"MOUNTJOY SQUARE WEST","address":"Mountjoy Square West","position_lat":53.356299,"position_lng":-6.258586,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391416000,"available_bike_stands":15,"available_bikes":15},"39":{"number":"29","contract_name":"dublin","name":"ORMOND QUAY UPPER","address":"Ormond Quay Upper","position_lat":53.346057,"position_lng":-6.268001,"banking":0,"bonus":0,"bike_stands":29,"status":"OPEN","last_update":1713391415000,"available_bike_stands":10,"available_bikes":19},"40":{"number":"3","contract_name":"dublin","name":"BOLTON STREET","address":"Bolton Street","position_lat":53.351182,"position_lng":-6.269859,"banking":0,"bonus":0,"bike_stands":20,"status":"OPEN","last_update":1713391440000,"available_bike_stands":12,"available_bikes":8},"41":{"number":"30","contract_name":"dublin","name":"PARNELL SQUARE NORTH","address":"Parnell Square North","position_lat":53.3537415547,"position_lng":-6.2653014478,"banking":0,"bonus":0,"bike_stands":20,"status":"OPEN","last_update":1713391402000,"available_bike_stands":19,"available_bikes":1},"42":{"number":"31","contract_name":"dublin","name":"PARNELL STREET","address":"Parnell Street","position_lat":53.350929,"position_lng":-6.265125,"banking":0,"bonus":0,"bike_stands":20,"status":"OPEN","last_update":1713391636000,"available_bike_stands":18,"available_bikes":2},"43":{"number":"32","contract_name":"dublin","name":"PEARSE STREET","address":"Pearse Street","position_lat":53.344304,"position_lng":-6.250427,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391636000,"available_bike_stands":12,"available_bikes":18},"44":{"number":"33","contract_name":"dublin","name":"PRINCES STREET \/ O'CONNELL STREET","address":"Princes Street \/ O'Connell Street","position_lat":53.349013,"position_lng":-6.260311,"banking":1,"bonus":0,"bike_stands":23,"status":"OPEN","last_update":1713391633000,"available_bike_stands":14,"available_bikes":8},"45":{"number":"34","contract_name":"dublin","name":"PORTOBELLO HARBOUR","address":"Portobello Harbour","position_lat":53.330362,"position_lng":-6.265163,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391408000,"available_bike_stands":1,"available_bikes":29},"46":{"number":"35","contract_name":"dublin","name":"SMITHFIELD","address":"Smithfield","position_lat":53.347692,"position_lng":-6.278214,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391423000,"available_bike_stands":28,"available_bikes":2},"47":{"number":"36","contract_name":"dublin","name":"ST. STEPHEN'S GREEN EAST","address":"St. Stephen's Green East","position_lat":53.337824,"position_lng":-6.256035,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391409000,"available_bike_stands":39,"available_bikes":1},"48":{"number":"37","contract_name":"dublin","name":"ST. STEPHEN'S GREEN SOUTH","address":"St. Stephen's Green South","position_lat":53.337494,"position_lng":-6.26199,"banking":1,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391403000,"available_bike_stands":30,"available_bikes":0},"49":{"number":"38","contract_name":"dublin","name":"TALBOT STREET","address":"Talbot Street","position_lat":53.350974,"position_lng":-6.25294,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391421000,"available_bike_stands":3,"available_bikes":37},"50":{"number":"39","contract_name":"dublin","name":"WILTON TERRACE","address":"Wilton Terrace","position_lat":53.332383,"position_lng":-6.252717,"banking":0,"bonus":0,"bike_stands":20,"status":"OPEN","last_update":1713391409000,"available_bike_stands":18,"available_bikes":2},"51":{"number":"4","contract_name":"dublin","name":"GREEK STREET","address":"Greek Street","position_lat":53.346874,"position_lng":-6.272976,"banking":0,"bonus":0,"bike_stands":20,"status":"OPEN","last_update":1713391422000,"available_bike_stands":10,"available_bikes":10},"52":{"number":"40","contract_name":"dublin","name":"JERVIS STREET","address":"Jervis Street","position_lat":53.3483,"position_lng":-6.266651,"banking":0,"bonus":0,"bike_stands":21,"status":"OPEN","last_update":1713391417000,"available_bike_stands":8,"available_bikes":13},"53":{"number":"41","contract_name":"dublin","name":"HARCOURT TERRACE","address":"Harcourt Terrace","position_lat":53.332763,"position_lng":-6.257942,"banking":0,"bonus":0,"bike_stands":20,"status":"OPEN","last_update":1713391408000,"available_bike_stands":11,"available_bikes":9},"54":{"number":"42","contract_name":"dublin","name":"SMITHFIELD NORTH","address":"Smithfield North","position_lat":53.349562,"position_lng":-6.278198,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391741000,"available_bike_stands":13,"available_bikes":17},"55":{"number":"43","contract_name":"dublin","name":"PORTOBELLO ROAD","address":"Portobello Road","position_lat":53.330091,"position_lng":-6.268044,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391565000,"available_bike_stands":1,"available_bikes":29},"56":{"number":"44","contract_name":"dublin","name":"UPPER SHERRARD STREET","address":"Upper Sherrard Street","position_lat":53.358437,"position_lng":-6.260641,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391411000,"available_bike_stands":17,"available_bikes":13},"57":{"number":"45","contract_name":"dublin","name":"DEVERELL PLACE","address":"Deverell Place","position_lat":53.351464,"position_lng":-6.255265,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391717000,"available_bike_stands":9,"available_bikes":21},"58":{"number":"47","contract_name":"dublin","name":"HERBERT STREET","address":"Herbert Street","position_lat":53.335742,"position_lng":-6.24551,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391409000,"available_bike_stands":40,"available_bikes":0},"59":{"number":"48","contract_name":"dublin","name":"EXCISE WALK","address":"Excise Walk","position_lat":53.347777,"position_lng":-6.244239,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391405000,"available_bike_stands":3,"available_bikes":37},"60":{"number":"49","contract_name":"dublin","name":"GUILD STREET","address":"Guild Street","position_lat":53.347932,"position_lng":-6.240928,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391407000,"available_bike_stands":33,"available_bikes":7},"61":{"number":"5","contract_name":"dublin","name":"CHARLEMONT PLACE","address":"Charlemont Street","position_lat":53.330662,"position_lng":-6.260177,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391703000,"available_bike_stands":0,"available_bikes":40},"62":{"number":"50","contract_name":"dublin","name":"GEORGES LANE","address":"George's Lane","position_lat":53.35023,"position_lng":-6.279696,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391602000,"available_bike_stands":27,"available_bikes":13},"63":{"number":"51","contract_name":"dublin","name":"YORK STREET WEST","address":"York Street West","position_lat":53.339334,"position_lng":-6.264699,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391422000,"available_bike_stands":40,"available_bikes":0},"64":{"number":"52","contract_name":"dublin","name":"YORK STREET EAST","address":"York Street East","position_lat":53.338755,"position_lng":-6.262003,"banking":0,"bonus":0,"bike_stands":32,"status":"OPEN","last_update":1713391627000,"available_bike_stands":32,"available_bikes":0},"65":{"number":"53","contract_name":"dublin","name":"NEWMAN HOUSE","address":"Newman House","position_lat":53.337132,"position_lng":-6.26059,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391425000,"available_bike_stands":40,"available_bikes":0},"66":{"number":"54","contract_name":"dublin","name":"CLONMEL STREET","address":"Clonmel Street","position_lat":53.336021,"position_lng":-6.26298,"banking":0,"bonus":0,"bike_stands":33,"status":"OPEN","last_update":1713391403000,"available_bike_stands":30,"available_bikes":3},"67":{"number":"55","contract_name":"dublin","name":"HATCH STREET","address":"Hatch Street","position_lat":53.33403,"position_lng":-6.260714,"banking":0,"bonus":0,"bike_stands":36,"status":"OPEN","last_update":1713391626000,"available_bike_stands":35,"available_bikes":1},"68":{"number":"56","contract_name":"dublin","name":"MOUNT STREET LOWER","address":"Mount Street Lower","position_lat":53.33796,"position_lng":-6.24153,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391638000,"available_bike_stands":38,"available_bikes":2},"69":{"number":"57","contract_name":"dublin","name":"GRATTAN STREET","address":"Grattan Street","position_lat":53.339629,"position_lng":-6.243778,"banking":0,"bonus":0,"bike_stands":23,"status":"OPEN","last_update":1713391627000,"available_bike_stands":12,"available_bikes":11},"70":{"number":"58","contract_name":"dublin","name":"SIR PATRICK DUN'S","address":"Sir Patrick's Dun","position_lat":53.339218,"position_lng":-6.240642,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391430000,"available_bike_stands":37,"available_bikes":3},"71":{"number":"59","contract_name":"dublin","name":"DENMARK STREET GREAT","address":"Denmark Street Great","position_lat":53.35561,"position_lng":-6.261397,"banking":0,"bonus":0,"bike_stands":20,"status":"OPEN","last_update":1713391406000,"available_bike_stands":14,"available_bikes":6},"72":{"number":"6","contract_name":"dublin","name":"CHRISTCHURCH PLACE","address":"Christchurch Place","position_lat":53.343368,"position_lng":-6.27012,"banking":0,"bonus":0,"bike_stands":20,"status":"OPEN","last_update":1713391424000,"available_bike_stands":17,"available_bikes":3},"73":{"number":"60","contract_name":"dublin","name":"NORTH CIRCULAR ROAD","address":"North Circular Road","position_lat":53.359624,"position_lng":-6.260348,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391411000,"available_bike_stands":0,"available_bikes":30},"74":{"number":"61","contract_name":"dublin","name":"HARDWICKE PLACE","address":"Hardwicke Place","position_lat":53.357043,"position_lng":-6.263232,"banking":0,"bonus":0,"bike_stands":25,"status":"OPEN","last_update":1713391628000,"available_bike_stands":16,"available_bikes":9},"75":{"number":"62","contract_name":"dublin","name":"LIME STREET","address":"Lime Street","position_lat":53.346026,"position_lng":-6.243576,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391583000,"available_bike_stands":31,"available_bikes":9},"76":{"number":"63","contract_name":"dublin","name":"FENIAN STREET","address":"Fenian Street","position_lat":53.341428,"position_lng":-6.24672,"banking":0,"bonus":0,"bike_stands":35,"status":"OPEN","last_update":1713391425000,"available_bike_stands":29,"available_bikes":6},"77":{"number":"64","contract_name":"dublin","name":"SANDWITH STREET","address":"Sandwith Street","position_lat":53.345203,"position_lng":-6.247163,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391667000,"available_bike_stands":9,"available_bikes":31},"78":{"number":"65","contract_name":"dublin","name":"CONVENTION CENTRE","address":"Convention Centre","position_lat":53.34744,"position_lng":-6.238523,"banking":1,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391402000,"available_bike_stands":37,"available_bikes":3},"79":{"number":"66","contract_name":"dublin","name":"NEW CENTRAL BANK","address":"New Central Bank","position_lat":53.347122,"position_lng":-6.234749,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391425000,"available_bike_stands":34,"available_bikes":6},"80":{"number":"67","contract_name":"dublin","name":"THE POINT","address":"The Point","position_lat":53.346867,"position_lng":-6.230852,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391551000,"available_bike_stands":16,"available_bikes":24},"81":{"number":"68","contract_name":"dublin","name":"HANOVER QUAY","address":"Hanover Quay","position_lat":53.344115,"position_lng":-6.237153,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391504000,"available_bike_stands":35,"available_bikes":5},"82":{"number":"69","contract_name":"dublin","name":"GRAND CANAL DOCK","address":"Grand Canal Dock","position_lat":53.342638,"position_lng":-6.238695,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391565000,"available_bike_stands":36,"available_bikes":4},"83":{"number":"7","contract_name":"dublin","name":"HIGH STREET","address":"High Street","position_lat":53.343565,"position_lng":-6.275071,"banking":0,"bonus":0,"bike_stands":29,"status":"OPEN","last_update":1713391423000,"available_bike_stands":15,"available_bikes":14},"84":{"number":"71","contract_name":"dublin","name":"KEVIN STREET","address":"Kevin Street","position_lat":53.337757,"position_lng":-6.267699,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391455000,"available_bike_stands":36,"available_bikes":4},"85":{"number":"72","contract_name":"dublin","name":"JOHN STREET WEST","address":"John Street West","position_lat":53.343105,"position_lng":-6.277167,"banking":0,"bonus":0,"bike_stands":31,"status":"OPEN","last_update":1713391212000,"available_bike_stands":28,"available_bikes":3},"86":{"number":"73","contract_name":"dublin","name":"FRANCIS STREET","address":"Francis Street","position_lat":53.342081,"position_lng":-6.275233,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391505000,"available_bike_stands":16,"available_bikes":14},"87":{"number":"74","contract_name":"dublin","name":"OLIVER BOND STREET","address":"Oliver Bond Street","position_lat":53.343893,"position_lng":-6.280531,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391662000,"available_bike_stands":19,"available_bikes":11},"88":{"number":"75","contract_name":"dublin","name":"JAMES STREET","address":"James Street","position_lat":53.343456,"position_lng":-6.287409,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391414000,"available_bike_stands":12,"available_bikes":28},"89":{"number":"76","contract_name":"dublin","name":"MARKET STREET SOUTH","address":"Market Street South","position_lat":53.342296,"position_lng":-6.287661,"banking":0,"bonus":0,"bike_stands":38,"status":"OPEN","last_update":1713391686000,"available_bike_stands":21,"available_bikes":17},"90":{"number":"77","contract_name":"dublin","name":"WOLFE TONE STREET","address":"Wolfe Tone Street","position_lat":53.348875,"position_lng":-6.267459,"banking":0,"bonus":0,"bike_stands":29,"status":"OPEN","last_update":1713391703000,"available_bike_stands":28,"available_bikes":1},"91":{"number":"78","contract_name":"dublin","name":"MATER HOSPITAL","address":"Mater Hospital","position_lat":53.359967,"position_lng":-6.264828,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391642000,"available_bike_stands":30,"available_bikes":10},"92":{"number":"79","contract_name":"dublin","name":"ECCLES STREET EAST","address":"Eccles Street East","position_lat":53.358115,"position_lng":-6.265601,"banking":0,"bonus":0,"bike_stands":27,"status":"OPEN","last_update":1713391635000,"available_bike_stands":27,"available_bikes":0},"93":{"number":"8","contract_name":"dublin","name":"CUSTOM HOUSE QUAY","address":"Custom House Quay","position_lat":53.347884,"position_lng":-6.248048,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391636000,"available_bike_stands":8,"available_bikes":22},"94":{"number":"80","contract_name":"dublin","name":"ST JAMES HOSPITAL (LUAS)","address":"St James Hospital (Luas)","position_lat":53.341359,"position_lng":-6.292951,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391709000,"available_bike_stands":28,"available_bikes":12},"95":{"number":"82","contract_name":"dublin","name":"MOUNT BROWN","address":"Mount Brown","position_lat":53.341645,"position_lng":-6.29719,"banking":0,"bonus":0,"bike_stands":22,"status":"OPEN","last_update":1713391404000,"available_bike_stands":11,"available_bikes":11},"96":{"number":"83","contract_name":"dublin","name":"EMMET ROAD","address":"Emmet Road","position_lat":53.340714,"position_lng":-6.308191,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391409000,"available_bike_stands":33,"available_bikes":7},"97":{"number":"84","contract_name":"dublin","name":"BROOKFIELD ROAD","address":"Brookfield Road","position_lat":53.339005,"position_lng":-6.300217,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391410000,"available_bike_stands":11,"available_bikes":19},"98":{"number":"85","contract_name":"dublin","name":"ROTHE ABBEY","address":"Rothe Abbey","position_lat":53.338776,"position_lng":-6.30395,"banking":0,"bonus":0,"bike_stands":35,"status":"OPEN","last_update":1713391412000,"available_bike_stands":6,"available_bikes":28},"99":{"number":"86","contract_name":"dublin","name":"PARKGATE STREET","address":"Parkgate Street","position_lat":53.347972,"position_lng":-6.291804,"banking":0,"bonus":0,"bike_stands":38,"status":"OPEN","last_update":1713391437000,"available_bike_stands":3,"available_bikes":35},"100":{"number":"87","contract_name":"dublin","name":"COLLINS BARRACKS MUSEUM","address":"Collins Barracks Museum","position_lat":53.347477,"position_lng":-6.28525,"banking":0,"bonus":0,"bike_stands":38,"status":"OPEN","last_update":1713391426000,"available_bike_stands":23,"available_bikes":15},"101":{"number":"88","contract_name":"dublin","name":"BLACKHALL PLACE","address":"Blackhall Place","position_lat":53.3488,"position_lng":-6.281637,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391411000,"available_bike_stands":13,"available_bikes":17},"102":{"number":"89","contract_name":"dublin","name":"FITZWILLIAM SQUARE EAST","address":"Fitzwilliam Square East","position_lat":53.335211,"position_lng":-6.2509,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391406000,"available_bike_stands":40,"available_bikes":0},"103":{"number":"9","contract_name":"dublin","name":"EXCHEQUER STREET","address":"Exchequer Street","position_lat":53.343034,"position_lng":-6.263578,"banking":0,"bonus":0,"bike_stands":24,"status":"OPEN","last_update":1713391681000,"available_bike_stands":21,"available_bikes":3},"104":{"number":"90","contract_name":"dublin","name":"BENSON STREET","address":"Benson Street","position_lat":53.344153,"position_lng":-6.233451,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391413000,"available_bike_stands":37,"available_bikes":3},"105":{"number":"91","contract_name":"dublin","name":"SOUTH DOCK ROAD","address":"South Dock Road","position_lat":53.341833,"position_lng":-6.231291,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391406000,"available_bike_stands":5,"available_bikes":25},"106":{"number":"92","contract_name":"dublin","name":"HEUSTON BRIDGE (NORTH)","address":"Heuston Bridge (North)","position_lat":53.347802,"position_lng":-6.292432,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391421000,"available_bike_stands":1,"available_bikes":39},"107":{"number":"93","contract_name":"dublin","name":"HEUSTON STATION (CENTRAL)","address":"Heuston Station (Central)","position_lat":53.346603,"position_lng":-6.296924,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391424000,"available_bike_stands":0,"available_bikes":40},"108":{"number":"94","contract_name":"dublin","name":"HEUSTON STATION (CAR PARK)","address":"Heuston Station (Car Park)","position_lat":53.346985,"position_lng":-6.297804,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391491000,"available_bike_stands":25,"available_bikes":15},"109":{"number":"95","contract_name":"dublin","name":"ROYAL HOSPITAL","address":"Royal Hospital","position_lat":53.343897,"position_lng":-6.29706,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391414000,"available_bike_stands":13,"available_bikes":27},"110":{"number":"96","contract_name":"dublin","name":"KILMAINHAM LANE","address":"Kilmainham Lane","position_lat":53.341805,"position_lng":-6.305085,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391407000,"available_bike_stands":13,"available_bikes":17},"111":{"number":"97","contract_name":"dublin","name":"KILMAINHAM GAOL","address":"Kilmainham Gaol","position_lat":53.342113,"position_lng":-6.310015,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391409000,"available_bike_stands":23,"available_bikes":17},"112":{"number":"98","contract_name":"dublin","name":"FREDERICK STREET SOUTH","address":"Frederick Street South","position_lat":53.341515,"position_lng":-6.256853,"banking":0,"bonus":0,"bike_stands":40,"status":"OPEN","last_update":1713391405000,"available_bike_stands":40,"available_bikes":0},"113":{"number":"99","contract_name":"dublin","name":"CITY QUAY","address":"City Quay","position_lat":53.346637,"position_lng":-6.246154,"banking":0,"bonus":0,"bike_stands":30,"status":"OPEN","last_update":1713391661000,"available_bike_stands":18,"available_bikes":12}}
        """
        mock_df = pd.read_json(stations_df, orient='index')
        mock_read_sql.return_value = mock_df
        # Make a test request to the stations endpoint
        response = self.app.get('/stations')

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check the content of the response, assuming it should return JSON
        response_json = json.loads(response.data)
        self.assertEqual(response_json['0']['name'], 'CLARENDON ROW')
        self.assertEqual(response_json['0']['number'], 1)

    @patch('pandas.read_sql_query')
    def test_get_weather(self, mock_read_sql):
        # Mocking the pandas read_sql_query function to return a dataframe
        mock_df = pd.DataFrame({
            'dt': [1708804200],
            'sunrise': [1708759439],
            'sunset': [1708797059],
            'temp': [278.55],
            'feels_like': [276.7],
            'pressure': [997],
            'humidity': [93],
            'uvi': [0.0],
            'clouds': [100],
            'visibility': [10000],
            'wind_speed': [2.3],
            'wind_deg': [120],
            'wind_gust': [2.2],
            'weather_main': ['Clouds'],
            'weather_description': ['overcast clouds'],
            'rain': [None],
            'snow': [None]
        })
        mock_read_sql.return_value = mock_df
        # Make a test request to the get_weather endpoint
        response = self.app.get('/weather/2024-02-25_10:38')

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check the content of the response
        self.assertIn('overcast clouds', response.data.decode())


if __name__ == '__main__':
    unittest.main()