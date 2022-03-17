
district = ["---- Select District ----", "Shimla", "Solan", "Police.Distt.Baddi", "Sirmaur", "Kinnaur",
            "Bilaspur", "Mandi", "Lahaul&Spiti", "Kullu", "Hamirpur", "Chamba",
            "Kangra", "Una", "Traffic, Tourist and Railway", "StateCID"]

stationdata = {"Shimla": {"Sadar Shimla":["Lakkar Baazar"], "East Shimla":["Kasumpti"], "New Shimla":[], "West Shimla":["Select","Jautogh","Summer Hill","Shoghi"],
                          "Dhalli":["Select","Junga","Sanjauli","Kufri"], "Sunni":["Tharu"], "Chopal":[], "Kupvi":[], "Kotkhai":[], "Theog":["Fagu"], "Deha":[], "Jhakri (PSOD)":["Select","Jeori","Sarahan"],
                          "Kumarsain":["Select","Narkanda","Sainj"], "Rampur":["Select","Rampur","Taklech"], "Jubbal":["Sawara-Kuddu"],
                           "Rohru":["Select","Dodra Kwar","Tikkar","Khadrala"], "Nerwa":[], "Chirgaon":["Select","Tangnu Romai","Jangla"], "Women P.S. Shimla":[], "Nankhari":[]},

               "Solan": {"Parwanoo":["T.P. Bhoj Nagar"], "Kasauli":["Garkhal","Kuthar"], "Sadar Solan":["City Solan","Saproon"], "Kandaghat":["Chail"], "Dharampur":["Subathu","Dagshai"], "Arki":["Sarli at Chhyod"], "Baga (PSOD)":[],
                         "Darlaghat":[], "Women P.S. Solan":[] , "Kunihar":["Sayari"]},

               "Police.Distt.Baddi": {"Nalagarh":["Joghon","Dabhota"], "Baddi":["Vardhman"], "Women P.S. Baddi":["Vardhman"], "Ramshahar":[], "Barotiwala":[], "Manpura":[]},

               "Sirmaur": {"Rajgarh":["Phajauta", "Yashwant Nagar"], "Pachhad":[], "Shillai":["Ronhat"], "Paonta":["Rajban","Singhpura"], "Renuka":["Nohra"], "Nahan":["Kacha Tank","Gunughat"], "Sangrah":["Haripurdhar"], "Kala Amb":["Trilokpur Temple"], "Women P.S.Nahan":[], "Majr":[], "Pruwala":[]},

               "Kinnaur": {"Rekong Peo":["T.P. Kalpa"], "Pooh":["Yangthang"], "Sangla":["T.P. Karchham"], "Bhawa Nagar":["Nichar(Sungra)"], "Tapri":["Nichar(Sungra)"], "Moorang":["Nichar(Sungra)"]},

               "Bilaspur": {"Bharari":[], "Ghumarwin":[], "Talai":[], "Barmana":["Nambhol","Kharsi(PSOD)"], "Sadar Bilaspur":["City"], "Swarghat":[], "Kot-Kehloor":["Naina Devi Ji","Golthai"], "Women P.S.Bilaspur":[], "Jhandutta":[]},

               "Mandi": {"Sundernagar":["Slaper","T.P. Dehar"], "Gohar":[], "Janjehli":[], "Karsog":["Pangna"], "Jogindernagar":["Ghatta","Bassi","T.p. Lad-Bhadol"], "Sarkaghat":[], "Dharampur":["Sandhol","Tihra"], "Sadar Mandi":["City Mandi","Pandoh","Kotli"], "Padhar":["Kamand","Tikkan"],
                         "Balh":["Rewalsar","Gagal"], "Aut":["T.P. Bali Chowki"], "BSL Colony Sundernagar":["Nihri"], "Women Police Station Mandi":[], "Hatli-Baldwara":[], "Dhanotu":[]},

               "Kullu": {"Nirmand":["Nither"], "Brow":[], "Ani":["Loohri"], "Manali":[], "Banjar":[], "Kullu":["Manikaran", "T.P. Akhara Bazar","T.P. Jari"], "Bhuntar":[], "Women Police Station at Kullu":[], "Sainj":[], "Patli-Kuhal":[]},

               "Lahaul&Spiti": {"Kaza":[], "Keylong":["Koksar(Sissu)","Jalman"], "Udaipur":["Tindi"]},

               "Hamirpur": {"Barsar":["Deothsidh"], "Sadar":["Tauni Devi"], "Bhoranj":["Jahu","Awahdevi"], "Nadaun":[], "Sujanpur":[], "Women P.S. Hamirpur":[]},

               "Chamba": {"Khairi":["Churah"], "Dalhousie":["Dalhousie","Baloon","T.P. Banikhet"], "Chowari":["Sihunta","Bakloh"], "Tissa":["T.P. Nakror"], "Kihar":["Surgani","Sanghani","T.P. Salooni"], "Sadar":["City Chambla","Drada","T.P. Sultanpur"], "Bharmaur":["Holi","Kutehr(PSOD Not)","T.P. Gehra"], "Pangi":["Purthy","Dharwas"], "Women P.S. Chamba":[]},

               "Kangra": {"Palampur":[], "Panchrukhi":[], "Lambagaon":["T.P. Alampur","T.P. Thural"], "Nurpur":["Sadwan","T.P. Rehan","T.P. Gangath","T.P. Kandwal"], "Indora":["Dhangupir", "Thakurwada"], "Damtal":["Dhangupir", "Thakurwada"], "Dehra":["Sansarpur Terrace","Dadasiba"], "Jawalaji":[], "Jawali":["Kotla", "T.P. Nagrota Surian"],
                          "Baijnath":["Chadhiyar","Multhan","Bir"], "Kangra":["Tnada","T.P. Lanj"], "Nagrota Bagwan":["Baroh"], "Dharamshala":["Yol"], "Mecleodganj":[], "Shahpur":["T.P. Darini"], "Haripur":["Ranital"], "Bhawarna":["T.P. Dheera"], "Fatehpur":["T.P. Rey"],
                          "Women P.S.Dharamshala":[], "P.S.Khundian":["Majheen","Lagru"], "Rakkar":[], "Gaggal":[]},

               "Una": {"Sadar Una":["Mehatpur","City Una"], "Haroli":["Santokhgarh","Pandoga","Tahliwal"], "Bangana":["Jol"], "Amb":[], "Gagret":["Daulatpur"], "Chintpurni":[], "Women P.S. Una":[]},

               "Traffic, Tourist and Railway": {"GRPS Shimla":["GROP Kandaghat"], "GRPS Kangra":["GROP Una","GROP Kandori"]},

               "StateCID" : {"State CID Shimla":[],"Cyber Crime Shimla":[]}

               }

battalion = ["1st HPABN Junga(Shimla)","1st IRBN Bangarh(Una)", "2nd IRBN Sakoh(Kangra)", "3rd IRBN Pandoh(Mandi)",
             "4th IRBN Jangal Beri(Hamirpur)", "5th IRBN Bassi(Bilaspur)", "6th IRBN Kolar(Sirmaur)"]

