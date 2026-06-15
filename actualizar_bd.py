import json
import re

print("⚙️ Iniciando la Trituradora de Datos Definitiva...")

texto_crudo = """
Guillaume Restes Francia Toulouse 19 POR 24.5M 78 88 +12.8% 8.8 / 10
Dennis Seimen Alemania Stuttgart 18 POR 3.2M 69 87 +26.0% 9.4 / 10
James Trafford Inglaterra Burnley 21 POR 10.5M 75 86 +14.6% 8.1 / 10
Bart Verbruggen Países Bajos Brighton 21 POR 16.5M 77 86 +11.6% 7.9 / 10
Lucas Chevalier Francia Lille 22 POR 24.0M 79 85 +7.5% 7.4 / 10
Jonas Urbig Alemania Köln 20 POR 8.0M 74 84 +13.5% 8.4 / 10
Filip Jörgensen Dinamarca Chelsea 22 POR 10.5M 75 84 +12.0% 7.8 / 10
Kjell Peersman Bélgica PSV 20 POR 1.6M 65 84 +29.2% 9.0 / 10
Rome-Jayden Owusu-Oduro Países Bajos AZ Alkmaar 19 POR 3.8M 71 83 +16.9% 8.6 / 10
Diego Kochen EE. UU. Barça Atlètic 18 POR 1.1M 63 83 +31.7% 9.2 / 10
Mio Backhaus Alemania Werder Bremen 20 POR 3.2M 70 83 +18.5% 8.5 / 10
Gavin Bazunu Irlanda Southampton 22 POR 5.5M 73 83 +13.6% 7.6 / 10
Alejandro Iturbe España Atlético Madrid 20 POR 2.5M 68 82 +20.5% 8.2 / 10
Oliver Dovin Suecia Coventry City 21 POR 2.7M 69 82 +18.8% 8.0 / 10
Chris Brady EE. UU. Chicago Fire 20 POR 2.7M 69 82 +18.8% 8.1 / 10
Noah Atubolu Alemania Freiburg 22 POR 7.5M 74 82 +10.8% 7.2 / 10
Mike Penders Bélgica Genk 18 POR 1.2M 64 82 +28.1% 8.9 / 10
Andrew Brasil Gil Vicente 23 POR 3.8M 72 81 +12.5% 7.3 / 10
Gregoire Swiderski Canadá Bordeaux 18 POR 650K 60 81 +35.0% 9.1 / 10
Spike Brits Inglaterra Man City 17 POR 650K 60 81 +35.0% 9.3 / 10
Leny Yoro Francia Man United 18 DFC 28.5M 78 89 +14.1% 9.0 / 10
Jorrel Hato Países Bajos Ajax 18 DFC / LI 21.0M 77 88 +14.2% 9.2 / 10
Giorgio Scalvini Italia Atalanta 20 DFC 28.5M 78 88 +12.8% 8.5 / 10
Pau Cubarsí España Barcelona 17 DFC 14.5M 75 88 +17.3% 9.4 / 10
Dean Huijsen España Bournemouth 19 DFC 10.5M 74 87 +17.5% 8.9 / 10
Ousmane Diomande Costa de Marfil Sporting CP 20 DFC 28.5M 78 87 +11.5% 8.3 / 10
Jarrad Branthwaite Inglaterra Everton 22 DFC 34.0M 80 86 +7.5% 7.8 / 10
Castello Lukeba Francia RB Leipzig 21 DFC 34.0M 79 86 +8.8% 8.0 / 10
Murillo Brasil Nottingham 22 DFC 34.0M 79 86 +8.8% 7.9 / 10
Zeno Debast Bélgica Sporting CP 20 DFC / LD 16.5M 76 86 +13.1% 8.2 / 10
Illia Zabarnyi Ucrania Bournemouth 21 DFC 34.0M 79 85 +7.5% 7.7 / 10
Cristhian Mosquera España Valencia 20 DFC 21.0M 77 85 +10.3% 8.4 / 10
Beraldo Brasil PSG 20 DFC / LI 21.0M 77 85 +10.3% 8.1 / 10
Yarek Gasiorowski España Valencia 19 DFC / LI 3.2M 69 84 +21.7% 9.0 / 10
Leandro Morgalla Alemania Salzburg 19 DFC / LD 3.8M 70 84 +20.0% 8.7 / 10
Benoît Badiashile Francia Chelsea 23 DFC 21.0M 77 84 +9.0% 7.2 / 10
Abdoulaye Ndiaye Senegal Troyes 22 DFC 5.5M 72 84 +16.6% 8.0 / 10
Tanguy Nianzou Francia Sevilla 22 DFC 6.5M 73 83 +13.7% 7.4 / 10
Chadi Riad Marruecos Crystal Palace 21 DFC 10.5M 75 83 +10.6% 7.9 / 10
Koni De Winter Bélgica Genoa 22 DFC / LD 10.5M 75 83 +10.6% 7.6 / 10
Arthur Chaves Brasil Hoffenheim 23 DFC 3.8M 71 83 +16.9% 7.8 / 10
Soungoutou Magassa Francia Monaco 20 DFC / MCD 5.5M 72 83 +15.2% 8.2 / 10
Mika Mármol España Las Palmas 23 DFC / LI 14.5M 76 83 +9.2% 7.5 / 10
Levi Colwill Inglaterra Chelsea 21 DFC / LI 21.0M 77 83 +7.7% 7.6 / 10
Malick Thiaw Alemania AC Milan 22 DFC 21.0M 77 83 +7.7% 7.7 / 10
Nathan Wood Inglaterra Southampton 22 DFC 3.2M 70 82 +17.1% 7.9 / 10
Anel Ahmedhodzic Bosnia Sheffield Utd 25 DFC 8.0M 75 82 +9.3% 7.1 / 10
Martin Vitik Rep. Checa Sparta Praha 21 DFC 10.5M 75 82 +9.3% 7.8 / 10
Strahinja Pavlovic Serbia AC Milan 23 DFC 14.5M 76 82 +7.8% 7.4 / 10
Alexander Aravena Chile Grêmio 22 DFC 5.5M 72 82 +13.8% 7.6 / 10
Aaron Anselmino Argentina Boca Juniors 19 DFC 4.2M 71 82 +15.4% 8.6 / 10
Tobias Palacio Argentina Argentinos Jrs 18 DFC 3.2M 69 82 +18.8% 8.8 / 10
Christian Mawissa Francia Monaco 19 DFC / LD 3.8M 70 81 +15.7% 8.3 / 10
Saël Kumbedi Francia Lyon 19 LD / DFC 4.2M 71 81 +14.0% 8.2 / 10
Jorne Spileers Bélgica Club Brugge 19 DFC 3.8M 70 81 +15.7% 8.1 / 10
Alejandro Balde España Barcelona 20 LI / LD 38.5M 80 89 +11.2% 8.6 / 10
Rico Lewis Inglaterra Man City 19 LD / MCD 21.0M 77 87 +12.9% 9.1 / 10
Destiny Udogie Italia Tottenham 21 LI 43.5M 81 86 +6.1% 7.9 / 10
Malo Gusto Francia Chelsea 21 LD 34.0M 80 86 +7.5% 8.3 / 10
Arnau Martínez España Girona 21 LD / DFC 16.5M 76 86 +13.1% 8.5 / 10
Milos Kerkez Hungría Bournemouth 20 LI 21.0M 77 86 +11.6% 8.4 / 10
Tino Livramento Inglaterra Newcastle 21 LD / LI 21.0M 77 85 +10.3% 8.2 / 10
Nuno Mendes Portugal PSG 24 LI 34.0M 80 84 +5.0% 7.1 / 10
Michael Kayode Italia Fiorentina 20 LD 9.0M 74 84 +13.5% 8.8 / 10
Ian Maatsen Países Bajos Aston Villa 22 LI 21.0M 77 84 +9.0% 7.8 / 10
Amar Dedic Bosnia Salzburg 21 LD / LI 11.5M 75 84 +12.0% 8.1 / 10
Bjorn Meijer Países Bajos Club Brugge 21 LI 7.0M 73 84 +15.0% 8.3 / 10
Filippo Terracciano Italia AC Milan 21 LD / LI 3.8M 70 84 +20.0% 8.5 / 10
Conor Bradley Irlanda N. Liverpool 21 LD 11.5M 75 83 +10.6% 8.3 / 10
Devyne Rensch Países Bajos Ajax 21 LD / LI 11.5M 75 83 +10.6% 8.0 / 10
Patrick Dorgu Dinamarca Lecce 19 LI 7.0M 73 83 +13.7% 8.7 / 10
Lewis Hall Inglaterra Newcastle 19 LI / MI 9.0M 74 83 +12.1% 8.4 / 10
Áxl Valle España Celtic 20 LI 3.8M 70 83 +18.5% 8.6 / 10
Joe Scally EE. UU. M'gladbach 21 LD / LI 8.0M 74 83 +12.1% 7.8 / 10
Quinten Timber Países Bajos Feyenoord 23 MC / LD 14.5M 76 83 +9.2% 7.4 / 10
Bradley Barcola Francia PSG 21 EI / ED 14.5M 76 83 +9.2% 7.9 / 10
Tiago Santos Portugal Lille 21 LD 11.5M 75 82 +9.3% 8.1 / 10
Cody Drameh Inglaterra Hull City 22 LD 4.2M 71 82 +15.4% 7.9 / 10
Josh Doig Escocia Sassuolo 22 LI 5.5M 72 82 +13.8% 7.7 / 10
Nathaniel Nwosu Nigeria Waterford 20 LD 1.0M 62 82 +32.2% 8.9 / 10
Jon Aramburu Venezuela Real Sociedad 21 LD / LI 5.5M 72 81 +12.5% 7.8 / 10
Marc Pubill España Almería 21 LD 7.0M 73 81 +10.9% 7.7 / 10
Agustín Giay Argentina Palmeiras 20 LD / MD 5.5M 72 81 +12.5% 8.0 / 10
Hugo Bueno España Feyenoord 21 LI 5.5M 72 81 +12.5% 7.9 / 10
Calvin Ramsay Escocia Wigan Athletic 21 LD 2.7M 68 83 +22.0% 8.5 / 10
Jude Bellingham Inglaterra Real Madrid 21 MC / MCO 135.5M 90 94 +4.4% 6.5 / 10
Florian Wirtz Alemania Leverkusen 21 MCO / EI 108.5M 88 93 +5.6% 7.0 / 10
Jamal Musiala Alemania Bayern München 21 MCO / EI 98.5M 87 93 +6.9% 7.2 / 10
Pedri España Barcelona 21 MC / MCO 87.5M 86 90 +4.6% 6.9 / 10
Gavi España Barcelona 19 MC / MCO 61.5M 83 90 +8.4% 8.1 / 10
Warren Zaïre-Emery Francia PSG 18 MC / MCD 38.5M 80 90 +12.5% 9.2 / 10
Eduardo Camavinga Francia Real Madrid 21 MCD / MC 61.5M 83 90 +8.4% 8.0 / 10
Arda Güler Turquía Real Madrid 19 MCO / ED 28.5M 78 90 +15.3% 9.3 / 10
Xavi Simons Países Bajos RB Leipzig 21 MCO / EI 61.5M 83 89 +7.2% 7.8 / 10
João Neves Portugal PSG 19 MCD / MC 38.5M 80 89 +11.2% 8.9 / 10
Kobbie Mainoo Inglaterra Man United 19 MC / MCD 21.0M 77 88 +14.2% 9.0 / 10
Arthur Vermeeren Bélgica RB Leipzig 19 MCD / MC 16.5M 76 87 +14.4% 8.8 / 10
Lucas Bergvall Suecia Tottenham 18 MC / MCO 4.5M 71 87 +22.5% 9.4 / 10
Lewis Miley Inglaterra Newcastle 18 MC / MCD 4.5M 71 87 +22.5% 9.3 / 10
Franco Mastantuono Argentina River Plate 16 MCO 3.8M 70 86 +22.8% 9.5 / 10
Claudio Echeverri Argentina River Plate 18 MCO 4.5M 71 86 +21.1% 9.1 / 10
Stefan Bajcetic España Salzburg 19 MCD / MC 5.5M 72 86 +19.4% 8.9 / 10
Archie Gray Inglaterra Tottenham 18 LD / MCD 7.0M 73 86 +17.8% 9.0 / 10
Pablo Torre España Barcelona 21 MCO / MC 9.0M 74 86 +16.2% 8.3 / 10
Desiré Doué Francia PSG 19 MCO / EI 16.5M 76 85 +11.8% 8.6 / 10
Carlos Baleba Camerún Brighton 20 MCD / MC 9.0M 74 85 +14.8% 8.5 / 10
Bilal El Khannouss Marruecos Leicester City 20 MCO 11.5M 75 85 +13.3% 8.4 / 10
Assan Ouédraogo Alemania RB Leipzig 18 MC / MCO 3.2M 69 85 +23.1% 9.2 / 10
Gabri Veiga España Al Ahli 22 MC / MCO 21.0M 77 85 +10.3% 7.4 / 10
Romeo Lavia Bélgica Chelsea 20 MCD 10.5M 75 85 +13.3% 8.2 / 10
Oscar Gloukh Israel Salzburg 20 MCO 16.5M 76 84 +10.5% 8.3 / 10
Martin Baturina Croacia Dinamo Zagreb 21 MC / MCO 16.5M 76 84 +10.5% 8.1 / 10
Kenneth Taylor Países Bajos Ajax 22 MC / MCD 16.5M 76 84 +10.5% 7.8 / 10
Gianluca Prestianni Argentina Benfica 18 ED / MCO 3.2M 69 84 +21.7% 9.1 / 10
Maurits Kjærgaard Dinamarca Salzburg 21 MC / MI 9.0M 74 84 +13.5% 8.0 / 10
Lazar Samardzic Serbia Atalanta 22 MC / MCO 21.0M 77 84 +9.0% 7.9 / 10
Tommaso Baldanzi Italia AS Roma 21 MCO / ED 11.5M 75 84 +12.0% 8.2 / 10
Javi Guerra España Valencia 21 MC 16.5M 76 83 +9.2% 8.0 / 10
Fermín López España Barcelona 21 MC / MCO 21.0M 77 83 +7.7% 8.1 / 10
Alex Scott Inglaterra Bournemouth 20 MC / MCO 9.0M 74 83 +12.1% 8.2 / 10
Samuele Ricci Italia Torino 22 MCD / MC 14.5M 76 83 +9.2% 7.9 / 10
Nicolò Fagioli Italia Juventus 23 MC / MCD 14.5M 76 83 +9.2% 7.5 / 10
Fabio Miretti Italia Genoa 20 MC / MCO 7.0M 73 83 +13.7% 8.1 / 10
Cher Ndour Italia Beşiktaş 19 MC / MCD 3.8M 70 83 +18.5% 8.4 / 10
Luis Guilherme Brasil West Ham 18 MD / MCO 4.5M 71 83 +16.9% 8.8 / 10
Sverre Nypan Noruega Rosenborg 17 MC / MCO 2.7M 68 83 +22.0% 9.2 / 10
Charlie Patino Inglaterra Deportivo 20 MC / MCD 3.8M 70 83 +18.5% 8.2 / 10
Mateus Fernandes Portugal Southampton 20 MC / MCO 7.0M 73 82 +12.3% 8.0 / 10
Hugo Larsson Suecia Eintracht 20 MC / MCD 9.0M 74 82 +10.8% 8.1 / 10
James Hackney Inglaterra Middlesbrough 21 MC / MCD 4.2M 71 82 +15.4% 7.9 / 10
Carney Chukwuemeka Inglaterra Chelsea 20 MCO / MC 5.5M 72 82 +13.8% 7.8 / 10
Elliot Anderson Escocia Nottingham 21 MC / MI 9.0M 74 82 +10.8% 7.6 / 10
Eduardo Bove Italia Fiorentina 22 MC / MCD 11.5M 75 82 +9.3% 7.4 / 10
Kristjan Asllani Albania Inter 22 MCD / MC 7.0M 73 82 +12.3% 7.5 / 10
Johan Bakayoko Bélgica PSV 21 ED 16.5M 76 82 +7.8% 7.3 / 10
Noah Lahmadi Francia Toulouse 19 MC / MCD 1.1M 63 82 +30.1% 8.9 / 10
Vasilije Adzic Montenegro Juventus 18 MCO / MC 1.6M 65 81 +24.6% 8.9 / 10
Assane Diao España Betis 18 EI / ED 4.2M 71 81 +14.0% 8.4 / 10
Pape Matar Sarr Senegal Tottenham 21 MC / MCD 11.5M 75 81 +8.0% 7.3 / 10
Lewis Warrington Inglaterra Leyton Orient 21 MCD / MC 1.1M 63 81 +28.5% 8.0 / 10
Endrick Brasil Real Madrid 19 DC / SD 24.5M 77 91 +18.1% 9.2 / 10
Evan Ferguson Irlanda Brighton 21 DC 10.5M 74 87 +17.5% 8.9 / 10
Mathys Tel Francia Bayern München 21 DC / EI 10.5M 74 87 +17.5% 9.0 / 10
George Ilenikhena Francia AS Monaco 19 DC 4.5M 71 83 +16.9% 9.3 / 10
Marc Guiu España Chelsea 20 DC 2.5M 67 82 +22.3% 8.9 / 10
Paris Brunner Alemania Cercle Brugge 20 DC / EI 1.8M 65 82 +26.1% 9.2 / 10
Vitor Roque Brasil Real Betis 21 DC 17.5M 76 86 +13.1% 8.4 / 10
Samu Omorodion España FC Porto 22 DC 17.5M 76 85 +11.8% 8.5 / 10
Youssoufa Moukoko Alemania OGC Nice 21 DC 10.5M 74 85 +14.8% 8.6 / 10
Júlio Enciso Paraguay Brighton 22 MCO / DC 7.0M 73 84 +15.0% 8.7 / 10
Alejo Véliz Argentina RCD Espanyol 22 DC 4.5M 71 83 +16.9% 8.4 / 10
Nelson Weiper Alemania Mainz 05 21 DC 2.1M 66 82 +24.2% 9.1 / 10
Jason van Duiven Países Bajos Lommel SK 21 DC 2.1M 66 82 +24.2% 8.8 / 10
Iker Bravo España Udinese 21 DC / SD 2.1M 66 81 +22.7% 8.5 / 10
Rodrigo Ribeiro Portugal Sporting CP 21 DC 2.9M 68 81 +19.1% 8.3 / 10
Rasmus Højlund Dinamarca Man United 23 DC 29.5M 78 88 +12.8% 8.3 / 10
Benjamin Šeško Eslovenia RB Leipzig 23 DC 34.0M 79 87 +10.1% 8.1 / 10
Maximilian Beier Alemania Borussia Dortmund 23 DC / ED 21.0M 77 84 +9.1% 7.9 / 10
Marcos Leonardo Brasil Al Hilal 23 DC 12.5M 75 84 +12.0% 8.0 / 10
Elye Wahi Francia Olympique Marseille 23 DC 14.5M 76 84 +10.5% 7.8 / 10
Matthis Abline Francia FC Nantes 23 DC 4.8M 72 81 +12.5% 7.6 / 10
Sékou Mara Francia RC Strasbourg 23 DC 3.8M 71 81 +14.0% 7.4 / 10
Matias Arezo Uruguay Grêmio 23 DC 3.8M 71 81 +14.0% 7.5 / 10
Santiago Giménez México Feyenoord 25 DC 26.5M 79 85 +7.6% 7.4 / 10
Karim Adeyemi Alemania Borussia Dortmund 24 DC / EI 14.5M 76 84 +10.5% 8.3 / 10
João Pedro Brasil Brighton 24 DC / MCO 21.0M 77 84 +9.1% 7.6 / 10
Folarin Balogun EE. UU. AS Monaco 24 DC 14.5M 76 83 +9.2% 7.3 / 10
Brian Brobbey Países Bajos Ajax 24 DC 14.5M 76 83 +9.2% 7.5 / 10
Arnaud Kalimuendo Francia Stade Rennais 24 DC 11.5M 75 82 +9.3% 7.2 / 10
Jovane Cabral Cabo Verde Estrela Amadora 28 EI / DC 2.5M 71 81 +14.0% 6.2 / 10
Lamine Yamal España Barcelona 18 ED 68.5M 81 94 +16.0% 8.8 / 10
Cole Palmer Inglaterra Chelsea 22 ED 62.5M 84 89 +5.9% 7.2 / 10
Nico Williams España Athletic 21 EI 52.5M 83 89 +7.2% 7.8 / 10
Savinho Brasil ManCity 20 ED 42.0M 81 88 +8.6% 8.0 / 10
Estêvão Brasil Chelsea 17 ED 28.5M 74 88 +12.8% 9.3 / 10
Julien Duranville Bélgica Dortmund 18 EI 11.5M 66 87 +31.8% 9.5 / 10
Kenan Yıldız Turquía Juventus 19 EI 24.5M 74 87 +17.5% 8.9 / 10
Alejandro Garnacho Argentina ManUnited 19 EI 34.0M 79 86 +8.8% 8.1 / 10
Jamie Gittens Inglaterra Dortmund 19 EI 14.5M 75 86 +14.6% 8.7 / 10
Yeremy Pino España Villarreal 21 ED 25.5M 78 86 +10.2% 7.9 / 10
Pedro Neto Portugal Chelsea 24 EI 29.0M 80 85 +6.2% 7.0 / 10
Ernest Nuamah Ghana Lyon 20 ED 10.5M 74 85 +14.8% 8.4 / 10
Ansu Fati España Barcelona 21 EI 14.0M 76 85 +11.8% 8.2 / 10
Noni Madueke Inglaterra Chelsea 22 ED 18.0M 77 84 +9.1% 7.5 / 10
Johan Bakayoko Bélgica PSV 21 ED 28.0M 79 84 +6.3% 7.1 / 10
Malick Fofana Bélgica Lyon 19 EI 7.5M 72 84 +16.6% 8.9 / 10
Badredine Bouanani Argelia Nice 19 ED 4.8M 70 84 +20.0% 9.0 / 10
Ilias Akhomach Marruecos Villarreal 20 ED 6.5M 73 84 +15.0% 8.5 / 10
Antonio Nusa Noruega Leipzig 19 EI 7.0M 73 83 +13.7% 8.3 / 10
Roony Bardghji Suecia Copenhague 18 ED 4.5M 71 83 +16.9% 8.8 / 10
Ibrahim Osman Ghana Feyenoord 19 EI 4.5M 71 83 +16.9% 8.6 / 10
Wilfried Gnonto Italia Leeds 20 EI 6.5M 73 83 +13.7% 8.2 / 10
Nico Paz Argentina Como 19 MCO 3.8M 70 83 +18.5% 9.1 / 10
Roger Fernandes Portugal Braga 18 ED 3.5M 70 83 +18.5% 9.2 / 10
Samuel Iling-Junior Inglaterra Bologna 20 EI 5.0M 72 83 +15.2% 8.4 / 10
Yankuba Minteh Gambia Brighton 19 ED 9.0M 74 82 +10.8% 7.8 / 10
Ben Doak Escocia Middlesbrough 18 ED 2.5M 67 82 +22.3% 9.4 / 10
Carlos Forbs Portugal Ajax 20 EI 4.2M 71 82 +15.4% 8.3 / 10
Nestory Irankunda Australia Bayern 18 ED 2.1M 66 82 +24.2% 9.5 / 10
Gianluca Prestianni Argentina Benfica 18 ED 3.2M 68 82 +20.5% 9.1 / 10
Brennan Johnson Gales Tottenham 23 ED 10.5M 76 81 +6.5% 7.1 / 10
Kamaldeen Sulemana Ghana Southampton 22 EI 5.5M 73 81 +10.9% 7.6 / 10
Facundo Pellistri Uruguay Panathinaikos 22 ED 5.5M 73 81 +10.9% 7.4 / 10
Matías Soulé Argentina Roma 21 ED 11.0M 76 81 +6.5% 7.2 / 10
Elias Saad Túnez St.Pauli 24 EI 3.5M 71 81 +14.0% 7.3 / 10
"""

jugadores_procesados = []

for linea in texto_crudo.split('\n'):
    linea = linea.strip()
    if not linea or "Jugador" in linea or "Bloque" in linea:
        continue
        
    linea_limpia = re.sub(r'\s+', ' ', linea)
    
    # Expresión regular robusta para extraer los datos desde atrás hacia adelante
    match = re.search(r'(\d+)\s+([A-Z/ ]+)\s+(\d+\.?\d*[MK])\s+(\d{2})\s+(\d{2})\s+\+?([\d\.]+)%\s+(\d\.\d)\s*/\s*10$', linea_limpia)
    
    if match:
        edad = int(match.group(1))
        pos = match.group(2).strip()
        valor_str = match.group(3)
        med = int(match.group(4))
        pot = int(match.group(5))
        roi = float(match.group(6))
        ganga = float(match.group(7))
        
        # Lo que queda al principio es: Nombre + Nacionalidad + Equipo
        resto = linea_limpia[:match.start()].strip()
        partes = resto.split()
        
        if len(partes) >= 3:
            nombre = " ".join(partes[:2])
            nacionalidad = partes[2]
            equipo = " ".join(partes[3:]) if len(partes) > 3 else "Desc."
        else:
            nombre = resto
            nacionalidad = "Desc."
            equipo = "Desc."
            
        # Convertir Valor a número entero
        if 'M' in valor_str:
            valor_real = int(float(valor_str.replace('M', '')) * 1000000)
        elif 'K' in valor_str:
            valor_real = int(float(valor_str.replace('K', '')) * 1000)
        else:
            valor_real = 0

        # Avatar dinámico
        nombre_url = nombre.replace(" ", "+")
        foto_url = f"https://ui-avatars.com/api/?name={nombre_url}&background=22c55e&color=fff&size=256&bold=true"

        jugadores_procesados.append({
            "Nombre": nombre,
            "Edad": edad,
            "Media": med,
            "Potencial": pot,
            "Posición": pos,
            "Equipo": equipo,
            "Nacionalidad": nacionalidad,
            "Valor Real (€)": valor_real,
            "Margen de Crecimiento": pot - med,
            "Ganga Score": ganga,
            "ROI (%)": roi,
            "Foto": foto_url
        })
    else:
        print(f"⚠️ Saltando línea irreconocible: {linea_limpia}")

with open('datos.py', 'w', encoding='utf-8') as f:
    f.write("# ==========================================\n")
    f.write("# BASE DE DATOS DEFINITIVA (FC 26)\n")
    f.write("# ==========================================\n\n")
    f.write("datos_reales = [\n")
    for j in jugadores_procesados:
        f.write(f"    {json.dumps(j, ensure_ascii=False)},\n")
    f.write("]\n")

print(f"✅ ¡Éxito! {len(jugadores_procesados)} jugadores exportados a datos.py")