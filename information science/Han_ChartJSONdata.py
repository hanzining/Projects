import urllib.request
import urllib.error
from urllib.error import URLError, HTTPError
import json
import gviz_api
import webbrowser

# This (big) string variable, delimited by triple quotes, contains the template
# for the HTML and JavaScript to render the chart.
# For more info, see https://developers.google.com/chart/interactive/docs/dev/gviz_api_lib
# Do NOT change this!
piechart_template = """
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable(%(json_text)s);

        var options = { 
        title: 'European Venture Capital Funds (EuVECA) Top Member States of the European Union (EU)', 
        colors: ['#aee5f2','#7fb2d4','#95dec5','#95dea2','#eef5a6','#f0c543','#aec2b7','#d2d6d4','#e0440e', '#e6693e', 
        '#ec8f6e', '#f3b49f', '#f6c7b6','#d3b2ed','#9a5dc9'], 
        pieHole: 0.3, 
        legend:'left', 
        width: 1200, 
        height: 800 }; 

        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="chart_div" style="width: 900px; height: 500px;"></div>
  </body>
</html>
"""

# can't combine the pieHole and is3D options; if you do, pieHole will be ignored

def main():
    # Parse the data of European Venture Capital Funds (EuVECA) registered in the Member States of the European Union
    # This function returns a dictionary of the different member countries in EU and their frequencies
    home_dictionary = parse_feed()
    description = [("homeMemberState", "string"), ("Frequency", "number")]

    # Create the data (in this case a list of tuples for each row)
    data = []

    for home in home_dictionary:
        data.append((home, home_dictionary[home]))

        # Create a DataTable object
        data_table = gviz_api.DataTable(description)
        data_table.LoadData(data)

        # Convert to JSON
        json_text = data_table.ToJSon()
        # print(json_text)

        # Create the html file with google pie chart
        filename = 'home_piechart.html'
        try:
            # Create HTML file
            html_file = open(filename, 'w', encoding='utf8')

            # Write the pie chart template to the file, substituting in the JSON text
            html_file.write(piechart_template % vars())

            # Open the HTML file in a browser (only works on Windows)
            # On Mac, open the generated HTML file, genre_piechart.html, in the PyCharm editor window,
            #   and select a browser from the icons in the upper right hand corner.
            webbrowser.open_new_tab(filename)

            # Close the file
            html_file.close()

        # error handling
        except ValueError as err:
            print(err)
        except FileNotFoundError as err:
            print(err)
        except OSError as err:
            print(err)
        # catch all error handler, if the above handlers do not apply
        except Exception as err:
            print(err)


def parse_feed():
    # create an empty dictionary to store the countries and frequencies
    home_dictionary = {}
    try:
        # get the most current information
        feed_url = "https://registers.esma.europa.eu/solr/esma_registers_euveca/select?q=*:*&rows=1000&wt=json&indent" \
                   "=true "
        feed_content = urllib.request.urlopen(feed_url).read().decode('utf8')

        # Parse the json data, extract and output information of interest
        feed_dictionary = json.loads(feed_content)

        response = feed_dictionary['response']
        # docs is a list, each of its element is a dictionary
        docs = response['docs']
        # print(docs)

        # only include the first 200 elements in the list
        # since some elements at the end of the list have missing 'homeMemberState' value which will cause an error
        for doc in docs[:200]:
            # get the value of member country in each dictionary using the key 'homeMemberState'
            home = doc['homeMemberState']
            # count the frequency of each member country and store into dictionary
            if home in home_dictionary:
                home_dictionary[home] += 1
            else:
                home_dictionary[home] = 1
        # print(home_dictionary)
        return home_dictionary

    # deal with url-related errors instead of file-related
    except ValueError as err:
        print('An error occurred trying to decode the json text')
        print(err)
    except HTTPError as err:
        print('Server could not fulfill the request.')
        print(err)
    except URLError as err:
        print('Failed to reach a server.')
        print(err)
        # catch all error handler, if the above handlers do not apply
    except Exception as err:
        print('An error occurred: ', err)


main()
