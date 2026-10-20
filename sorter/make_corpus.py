"""Build a small synthetic corpus of fictional public profiles and 32 find-this-person queries.
Every person here is invented. No real people, no scraping."""
import json, random
random.seed(7)
P = []
def add(pid, name, headline, city, body):
    P.append({"id": pid, "name": name, "headline": headline, "city": city, "body": body})

# Name collisions and near collisions are on purpose: that is where agents slip.
add("p01","Priya Raman","Staff engineer at Lumen Freight","Austin","Priya builds routing software for trucking. Before Lumen she spent four years at Ostrava Maps. Speaks at RustConf about allocators.")
add("p02","Priya Raman","Pediatric nurse","Austin","Priya Raman works night shifts at St. Brigid Children's. Runs a weekend 10k club. No software background.")
add("p03","Priya Ramanathan","Founder, Kestrel Health","Boston","Priya Ramanathan started Kestrel Health after a PhD in biostatistics. Kestrel sells claim audits to clinics.")
add("p04","Tomas Lindqvist","Head of data at Brightwell Bank","Stockholm","Tomas leads a team of 12 analysts. He previously worked at Ostrava Maps on geocoding. Maintains the open source library tidyledger.")
add("p05","Tomas Lindquist","Carpenter and furniture maker","Minneapolis","Tomas Lindquist makes walnut tables. Teaches a joinery class on Saturdays.")
add("p06","Ama Mensah","Product designer at Fernway","Accra","Ama designs onboarding flows. Former intern at Lumen Freight. Writes a newsletter called Small Screens.")
add("p07","Ama Mensah-Boateng","VP Marketing at Cobalt Ice","London","Ama Mensah-Boateng runs brand for a frozen dessert company. Joined from Unilever-style CPG roles.")
add("p08","Daniel Okafor","ML engineer at Quarry AI","San Francisco","Daniel trains ranking models. Ex Fernway. Co-author of a paper on retrieval for tabular data.")
add("p09","Daniel Okafor","Partner at Okafor and Reyes LLP","Lagos","Daniel Okafor practices commercial law. Sits on the board of a youth chess league.")
add("p10","Dani Okafor","Barista and illustrator","Portland","Dani Okafor draws comics about coffee. Sells prints online.")
add("p11","Mei Chen","CTO at Harbor Ledger","Singapore","Mei Chen co-founded Harbor Ledger, a payments reconciliation startup, in 2021. Previously principal engineer at Brightwell Bank.")
add("p12","Mei Chen","High school chemistry teacher","Vancouver","Mei Chen teaches AP chemistry. Coaches the robotics team.")
add("p13","Mei Chen-Watts","Recruiter at Quarry AI","San Francisco","Mei Chen-Watts hires ML engineers. Hosts a podcast about interviewing.")
add("p14","Rafael Duarte","Security researcher","Lisbon","Rafael finds bugs in payment SDKs. Formerly at Harbor Ledger. Known handle: rduarte_sec.")
add("p15","Rafael Duarte","Chef and owner of Casa Duarte","Porto","Rafael Duarte runs a seafood restaurant. Won a regional award in 2023.")
add("p16","Hana Sato","Engineering manager at Ostrava Maps","Tokyo","Hana manages the search team at Ostrava Maps. Previously at Quarry AI. Organizes a monthly Go meetup.")
add("p17","Hana Satou","Violinist","Osaka","Hana Satou plays with a chamber orchestra.")
add("p18","Lukas Becker","Founder of Spindle CRM","Berlin","Lukas started Spindle CRM in 2022 after selling a small analytics shop. Angel investor in Fernway.")
add("p19","Lukas Becker","Logistics coordinator at Lumen Freight","Hamburg","Lukas Becker schedules cross dock transfers. Works with the routing team.")
add("p20","Lucas Baker","Sales lead at Spindle CRM","Berlin","Lucas Baker sells CRM seats to mid market firms. Ex Cobalt Ice.")
add("p21","Sofia Marquez","Data scientist at Kestrel Health","Boston","Sofia builds risk models for claim audits. Ex Brightwell Bank analyst. Rock climber.")
add("p22","Sofia Marquez","Real estate agent","Miami","Sofia Marquez sells condos in Brickell.")
add("p23","Arjun Mehta","Open source maintainer of tidyledger","Pune","Arjun co-maintains tidyledger with Tomas Lindqvist. Works as a contractor for Harbor Ledger.")
add("p24","Arjun Mehta","Cardiologist","Mumbai","Dr. Arjun Mehta practices at a heart institute.")
add("p25","Arjun Mehra","Product manager at Fernway","Bangalore","Arjun Mehra owns the payments roadmap at Fernway.")
add("p26","Noor Haddad","Head of research at Quarry AI","Toronto","Noor leads the research group. PhD in information retrieval. Previously a scientist at Ostrava Maps.")
add("p27","Noor Haddad","Journalist covering energy","Amman","Noor Haddad writes about oil and solar markets.")
add("p28","Ivan Petrov","Site reliability engineer at Harbor Ledger","Sofia","Ivan runs on call for the ledger. Ex Lumen Freight. Writes about Postgres failover.")
add("p29","Ivan Petrov","Hockey coach","Toronto","Ivan Petrov coaches junior hockey.")
add("p30","Grace Kim","General partner at Northbeam Ventures","New York","Grace invests in fintech. Led the seed in Harbor Ledger and Spindle CRM.")
add("p31","Grace Kim","UX researcher at Cobalt Ice","Seoul","Grace Kim runs taste tests and user interviews.")
add("p32","Grace Kimball","Author","New York","Grace Kimball writes mystery novels.")
add("p33","Omar Farouk","Founder of Tilepath","Cairo","Omar built Tilepath, a map tile CDN. Sold it to Ostrava Maps in 2024. Now advises startups.")
add("p34","Omar Farouk","Accountant","Dubai","Omar Farouk audits small businesses.")
add("p35","Elena Rossi","COO at Fernway","Milan","Elena runs operations at Fernway. Ex McKinsey style consultant. Board member at Kestrel Health.")
add("p36","Elena Rossi","Fashion photographer","Milan","Elena Rossi shoots for magazines.")
add("p37","Kwame Asante","Platform engineer at Spindle CRM","Accra","Kwame runs the Kubernetes platform at Spindle CRM. Former Lumen Freight SRE.")
add("p38","Kwame Asante","Football agent","Kumasi","Kwame Asante represents young footballers.")
add("p39","Julia Novak","Principal engineer at Brightwell Bank","Prague","Julia replaced Mei Chen as principal engineer. Works on the core ledger.")
add("p40","Julia Nowak","Dentist","Krakow","Julia Nowak runs a family dental practice.")
# filler profiles that share employer words, to crowd the search results
fill_roles=["Account executive","Support engineer","Office manager","Intern","Designer","Analyst","Data engineer","Recruiter"]
cos=["Lumen Freight","Fernway","Quarry AI","Harbor Ledger","Ostrava Maps","Brightwell Bank","Spindle CRM","Kestrel Health"]
first=["Alex","Sam","Jordan","Taylor","Riley","Casey","Morgan","Jamie","Avery","Quinn","Rowan","Sky"]
last=["Hale","Moreau","Ivanova","Nakamura","Silva","Byrne","Kowal","Adeyemi","Larsen","Ortiz","Varga","Tan"]
for i in range(24):
    co=cos[i%8]; role=fill_roles[i%len(fill_roles)]
    add(f"f{i:02d}",f"{first[i%12]} {last[(i*5)%12]}",f"{role} at {co}",random.choice(["Austin","Berlin","Boston","San Francisco","Singapore","Tokyo","London"]),
        f"Works at {co} as {role.lower()}. Previously at {cos[(i+3)%8]}. Mentions search, routing, ledger and payments in posts.")

Q = [
 ("q01","Find Priya Raman, the engineer who builds trucking routing software.","p01"),
 ("q02","Find the Priya Raman who is a nurse in Austin.","p02"),
 ("q03","Who founded Kestrel Health?","p03"),
 ("q04","Find the head of data at Brightwell Bank who maintains tidyledger.","p04"),
 ("q05","Find Tomas Lindquist the furniture maker.","p05"),
 ("q06","Find the Fernway product designer who once interned at Lumen Freight.","p06"),
 ("q07","Find Daniel Okafor who works on ranking models.","p08"),
 ("q08","Find the lawyer named Daniel Okafor.","p09"),
 ("q09","Find the co-founder and CTO of Harbor Ledger.","p11"),
 ("q10","Find Mei Chen who used to be principal engineer at Brightwell Bank.","p11"),
 ("q11","Find the security researcher who goes by rduarte_sec.","p14"),
 ("q12","Find the person who manages the search team at Ostrava Maps.","p16"),
 ("q13","Find Lukas Becker, the founder of a CRM startup.","p18"),
 ("q14","Find the Lukas Becker who works in logistics in Hamburg.","p19"),
 ("q15","Find the data scientist at Kestrel Health who used to be an analyst at Brightwell Bank.","p21"),
 ("q16","Find Arjun Mehta who co-maintains tidyledger.","p23"),
 ("q17","Find the product manager for payments at Fernway.","p25"),
 ("q18","Find Noor Haddad, the information retrieval researcher.","p26"),
 ("q19","Find the Harbor Ledger SRE who writes about Postgres failover.","p28"),
 ("q20","Find the investor who led the seed round in Harbor Ledger.","p30"),
 ("q21","Find Grace Kim who does user research for a dessert company.","p31"),
 ("q22","Who sold a map tile CDN to Ostrava Maps?","p33"),
 ("q23","Find the COO of Fernway.","p35"),
 ("q24","Find Elena Rossi who sits on the Kestrel Health board.","p35"),
 ("q25","Find the platform engineer at Spindle CRM who used to be an SRE at Lumen Freight.","p37"),
 ("q26","Who replaced Mei Chen as principal engineer at Brightwell Bank?","p39"),
 ("q27","Find the Spindle CRM salesperson who used to work at Cobalt Ice.","p20"),
 ("q28","Find the person at Quarry AI who hires ML engineers.","p13"),
 ("q29","Find the head of research at Quarry AI.","p26"),
 ("q30","Find the Ivan Petrov who coaches hockey.","p29"),
 ("q31","Find the angel investor in Fernway who founded a CRM company.","p18"),
 ("q32","Find the person who co-maintains tidyledger and contracts for Harbor Ledger.","p23"),
]
json.dump(P, open("data/profiles.json","w"), indent=1)
# Keep any held-out queries already in the file (q33 and up). q01-q32 are dev:
# their traces were read during error analysis, so they cannot be held out.
import os
kept = []
if os.path.exists("data/queries.jsonl"):
    kept = [json.loads(l) for l in open("data/queries.jsonl") if json.loads(l)["split"] == "heldout"]
with open("data/queries.jsonl","w") as f:
    for qid,q,g in Q:
        f.write(json.dumps({"id":qid,"query":q,"gold":g,"split":"dev"})+"\n")
    for r in kept:
        f.write(json.dumps(r)+"\n")
print(len(P),"profiles",len(Q),"queries")
