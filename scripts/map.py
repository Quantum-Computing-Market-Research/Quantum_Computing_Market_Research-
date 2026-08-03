import pandas as pd 
import folium

df = pd.read_csv('data/quantum_DMV.csv')

locations = {
    "NIST (Gaithersburg)": [39.1406, -77.2189],
    
    "UMD: LPS Qubit Collaboratory": [38.9897, -76.9378],
    "UMD: The National Quantum Laboratory (QLab)": [38.9897, -76.9378],
    "UMD: Quantum Materials Center (QMC)": [38.9897, -76.9378],
    "UMD: Condensed Matter Theory Center": [38.9897, -76.9378],
    "UMD: QuICS": [38.9897, -76.9378],
    "UMD: Joint Quantum Institute (JQI)": [38.9897, -76.9378],
    "UMD: Quantum Technology Center (QTC)": [38.9897, -76.9378],

    "Johns Hopkins APL": [39.1653, -76.8967],

    "Howard University Quantum Lab": [38.9220, -77.0198],

    "Lockheed Martin (Bethesda)": [38.9847, -77.0947],

    "IonQ (College Park)": [38.9897, -76.9378],
    "Naval Research Laboratory (NRL)": [38.8239, -77.0233],
    "MITRE Corporation (McLean)": [38.9248, -77.2023]
} 

df['Latitude'] = df["Institution"].map(lambda x: locations.get(x, [None, None])[0])
df['Longitude'] = df["Institution"].map(lambda x: locations.get(x, [None,None])[1])

def trl_color(trl):
    trl = str(trl).replace("TRL", "").strip()
    trl = int(trl.split("-")[0])
    
    if trl <= 3:
        return "blue"
    elif trl <= 6:
        return "purple"
    else:
        return "red"
    
m = folium.Map(
    location= [39.0,-77.05],
    zoom_start=9,
    tiles="CartoDB positron"
)    

top_banner = """
<div style="
position: fixed;
top: 10px;
left: 50%;
transform: translateX(-50%);
width: 720px;
background: rgba(255,255,255,0.95);
padding: 12px;
border-radius: 10px;
box-shadow: 0 2px 10px rgba(0,0,0,0.3);
z-index:9999;
font-family:Arial;
">

<h3 style="margin:0;text-align:center;">
🏆 Top Quantum Cybersecurity Institutions
</h3>

<table style="width:100%;margin-top:8px;font-size:14px;">
<tr>
<th align="left">Rank</th>
<th align="left">Institution</th>
<th align="left">Focus</th>
</tr>

<tr>
<td>🥇</td>
<td><b>University of Maryland</b></td>
<td>PQC • QKD • Quantum Computing</td>
</tr>

<tr>
<td>🥈</td>
<td><b>NIST</b></td>
<td>PQC Standards • Networking</td>
</tr>

<tr>
<td>🥉</td>
<td><b>Johns Hopkins APL</b></td>
<td>Quantum Sensing • Secure Communications</td>
</tr>

</table>

</div>
"""

m.get_root().html.add_child(folium.Element(top_banner))

for _, row in df.iterrows():

    popup = f"""
    <h4>{row['Institution']}</h4>

    <b>Research Area:</b><br>
    {row['Research Area']}
    <br><br>

    <b>Technology Readiness:</b><br>
    {row['TRL']}
    <br><br>

    <b>Description:</b><br>
    {row['Description']}
    """

    
    folium.CircleMarker(
        location=[
            row["Latitude"],
            row["Longitude"]
        ],

        radius=10,

        color=trl_color(row["TRL"]),

        fill=True,

        fill_opacity=0.8,

        popup=folium.Popup(
            popup,
            max_width=350
        )

    ).add_to(m)
    
    legend = """
<div style="
position: fixed;
bottom: 40px;
left: 40px;
width: 220px;
background:white;
padding:15px;
border:2px solid grey;
z-index:9999;
">

<h4>Quantum TRL</h4>

<p>
<span style="color:blue;">●</span>
TRL 1-3 Fundamental Research
</p>

<p>
<span style="color:purple;">●</span>
TRL 4-6 Prototype / Applied
</p>

<p>
<span style="color:red;">●</span>
TRL 7-9 Deployment
</p>

</div>
"""


m.get_root().html.add_child(
    folium.Element(legend)
)

m.save("DMV_quantum_ecosystem_map.html")


print("Map saved!")
print(df[["Institution","Latitude","Longitude"]])