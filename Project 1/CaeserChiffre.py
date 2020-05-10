import numpy as np
def cVerschluesseln(text: str, schluessel: chr):
    repl = [chr(228), 'ae', chr(246), 'oe', chr(252), 'ue', chr(223), 'ss', " ", "", "\n", ""]
    if (len(repl) % 2 == 1):
        print("Nicht genug Argumente zum Austausch.")
        return
    for i in range(0,len(repl), 2):
        text = text.replace(repl[i], repl[i+1])
        text = text.replace(repl[i].upper(), repl[i+1].upper())
    erg = ""
    key = ord(schluessel) - ord('A') if (schluessel.isupper()) else ord(schluessel) - ord('a')
    for i in text:
        if(i.isalpha()):
            oMax = 90 if(i.isupper()) else 122
            if(ord(i) + key > oMax):
                next = ord(i) + key - 26
                erg += "".join(chr(next))
            else:
                erg += "".join(chr(ord(i)+key))
    print(erg)
    return(erg)

def cEntschluesseln(text: str, schluessel: chr):
    erg = ""
    key = ord(schluessel) - ord('A') if (schluessel.isupper()) else ord(schluessel) - ord('a')
    for i in text:
        oMin = 65 if (i.isupper()) else 97
        if(ord(i) - key < oMin):
            next = ord(i) - key + 26
            erg += "".join(chr(next))
        else:
            erg += "".join(chr(ord(i)-key))
    #print(erg)
    return erg

def ohneSchluessel(text: str):
    anz = np.zeros((26))
    m = text.upper()
    for i in m:
        stelle = ord(i) - 65
        anz[stelle] += 1
    #größte Häufigkeit + 65 für ASCII - 4 für Stelle E
    key = chr(np.argmax(anz)+65-4)
    loes = cEntschluesseln(text, key)
    return loes

def main():
    text = "Erster Versuch"
    textKappe = """Margarethenhoehe

    Die Margarethenhoehe ist ein suedlicher Stadtteil der Stadt Essen. Dessen Kern bildet die Siedlung Margarethenhoehe, die als erste deutsche Gartenstadt gilt.
    Die 115 Hektar grosse, von der Margarethe Krupp-Stiftung verwaltete Siedlung gilt als Beispiel fuer menschenfreundliches Wohnen. Sie verfuegt in 935 Gebaeuden ueber 3092 Wohneinheiten. 50 Hektar der Siedlungsflaeche sind als unbebaubares Waldland festgelegt.
    
    Geschichte
    Das Gebiet gehoert zur Gemarkung Ruettenscheid, das 1905 zur Stadt Essen eingemeindet wurde. Die ersten Haeuser auf der Hoehe wurden 1910 fertiggestellt, so dass die Bewohner von Beginn an Buerger der Stadt Essen waren. Die Margarethenhoehe wurde 1906 von Margarethe Krupp anlaesslich der Hochzeit ihrer Tochter Bertha gestiftet und ab 1906 bis 1938 von dem Architekten Georg Metzendorf (1874–1934), einem Mitglied des Deutschen Werkbundes, erbaut. Waehrend der Zeit ihrer Errichtung war sie, wie sonst nur die Gartenstadt Dresden-Hellerau, durch einen Regierungserlass von allen Bauvorschriften befreit. Die ersten Haeuser auf der Hoehe wurden 1910 fertiggestellt. Zuvor wurde 1909 der Viadukt ueber das Borbecker Muehlenbachtal errichtet, um eine Anbindung an die zentralen Siedlungsgebiete Holsterhausen und Ruettenscheid zu haben, das neue Gelaende zu erschliessen und es mit Baustoffen versorgen zu koennen. Der Viadukt fuehrte auch ueber die 1872 eroeffnete Bahnstrecke Muelheim-Heissen–Altendorf (Ruhr), an der es zwischen 1946 und 1965 den Personenbahnhof Margarethenhoehe gab, dessen Empfangsgebaeude abgerissen wurde. Die Bahntrasse wurde schliesslich 1999 endgueltig stillgelegt und darauf ein Radwanderweg angelegt.
    
    1924 erhielt die Margarethenhoehe eine katholische Kirche, die im Zweiten Weltkrieg 1944 zerstoert wurde. 1952 wurde die heutige katholische Kirche Heilige Familie geweiht, die seit 2008 Gemeindekirche der Pfarrgemeinde St. Antonius ist.
    
    Nach dem Zweiten Weltkrieg wurde die in grossen Teilen zerstoerte Siedlung in ihrer historischen Form wiederhergestellt. 1948 wurde die Margarethenhoehe ein eigenstaendiger Stadtteil. Von 1962 bis 1966 und von 1971 bis 1980 wurde auf dem noch unbebauten Land suedlich der ersten Siedlung die Margarethenhoehe II errichtet, architektonisch teils minderwertig, und speziell im letzten Bauabschnitt, in dem Hochhaeuser gebaut wurden, sozial problematisch. Laut Stiftung setzen diese Haeuser „einen deutlichen gestalterischen Kontrast zur alten Margarethenhoehe“. Um die sozialen, technischen und aesthetischen Probleme der Margarethenhoehe II zu beheben, wurde bereits 1987 ein Sanierungsprogramm begonnen, um die oeffentliche Wertschaetzung auch der juengeren Siedlungseinheit der Margarethenhoehe deutlich zu erhoehen.
    
    Die Margarethenhoehe I hingegen wurde 1987 unter Denkmalschutz gestellt. Eine vom Ruhr Museum eingerichtete Musterwohnung vergegenwaertigt dem Besucher die urspruengliche Gestaltung der Wohneinheiten und soll ihm „die wohnkulturelle Bedeutung des Denkmals Margarethenhoehe mit ihren variablen Typengrundrissen auch aus der Innenperspektive sichtbar werden“ lassen.
    
    Zeitweise existierte auf der Margarethenhoehe auch eine kleine Kuenstlerkolonie, deren bedeutendster Gast der Fotograf Albert Renger-Patzsch war. Diese Kolonie wurde in den 1930er Jahren aufgeloest, nur die Keramikwerkstatt Margarethenhoehe existiert noch. Sie ist nach 1933 in die Zeche Zollverein umgezogen. Die damalige Gelsenkirchener Bergwerksverein A.G. stellte zu diesem Zweck auf einem Zechengelaende diverse Raeumlichkeiten zur Verfuegung.
    
    Der Heimatforscher Hugo Rieth (1922–2006) war Chronist der Gartenstadt Margarethenhoehe. Seine Veroeffentlichungen in Zeitungen und Jahrbuechern belegen seine fundierten historischen Sachkenntnisse, fuer die ihm zu seinen Lebzeiten Ehrungen zuteilwurden, so unter anderem der Rheinlandtaler und das Bundesverdienstkreuz. Hugo Rieth verfuegte ueber eine umfangreiche Bibliothek mit Dokumenten, Aufzeichnungen und weiteren historisch bedeutungsvollen Belegen, sowie eine umfangreiche Fotosammlung, die nach seinem Tode in Teilen dem Stadtarchiv Essen, der Buergerschaft Margarethenhoehe und dem Essener Luftfahrtarchiv uebereignet worden sind."""
    textKappeCry = cVerschluesseln(textKappe, "H")
    #testText = 'ThynhylaoluovlolKplThynhylaoluovlolpzalpuzblkspjolyZahkaalpsklyZahkaLzzluKlzzluRlyuipsklakplZplksbunThynhylaoluovlolkplhszlyzalklbazjolNhyaluzahkanpsaKplOlrahynyvzzlcvuklyThynhylaolRybwwZapmabunclydhsalalZplksbunnpsahszIlpzwplsmblytluzjolumylbukspjolzDvouluZplclymblnapuNlihlbklublilyDvoulpuolpaluOlrahyklyZplksbunzmshljolzpukhszbuilihbihylzDhskshukmlzanlslnaNlzjopjoalKhzNliplanlovlyagbyNlthyrbunYblaaluzjolpkkhzgbyZahkaLzzlulpunltlpukladbyklKpllyzaluOhlbzlyhbmklyOvloldbyklumlyapnnlzalssazvkhzzkplIldvoulycvuIlnpuuhuIblynlyklyZahkaLzzludhyluKplThynhylaoluovloldbyklcvuThynhylaolRybwwhushlzzspjoklyOvjoglpapoylyAvjoalyIlyaohnlzapmalabukhiipzcvukltHyjopalraluNlvynTlaglukvymlpultTpansplkklzKlbazjoluDlyribuklzlyihbaDhloylukklyGlpapoylyLyypjoabundhyzpldplzvuzaubykplNhyaluzahkaKylzkluOlsslyhbkbyjolpuluYlnplybunzlyshzzcvuhssluIhbcvyzjoypmaluilmylpaKpllyzaluOhlbzlyhbmklyOvloldbyklumlyapnnlzalssaGbcvydbyklklyCphkbrablilykhzIvyiljrlyTblosluihjoahslyypjoalabtlpulHuipukbunhukplgluayhsluZplksbunznliplalOvszalyohbzlubukYblaaluzjolpkgbohilukhzulblNlshluklgblyzjosplzzlubuklztpaIhbzavmmluclyzvynlugbrvluuluKlyCphkbrambloyalhbjoblilykpllyvlmmulalIhouzayljrlTblsolptOlpzzluHsalukvymYboyhuklylzgdpzjolubukkluWlyzvuluihouovmThynhylaoluovlolnhiklzzluLtwmhunznlihlbklhinlypzzludbyklKplIhouayhzzldbyklzjosplzzspjoluknblsapnzapssnlslnabukkhyhbmlpuYhkdhuklydlnhunlslnalyoplsakplThynhylaoluovlollpulrhaovspzjolRpyjolkplptGdlpaluDlsaryplnglyzavlyadbykldbyklkplolbapnlrhaovspzjolRpyjolOlpspnlMhtpsplnldlpoakplzlpaNltlpuklrpyjolklyWmhyynltlpuklZaHuavupbzpzaUhjokltGdlpaluDlsaryplndbyklkplpunyvzzluAlpsluglyzavlyalZplksbunpupoylyopzavypzjoluMvytdplklyolynlzalssadbyklkplThynhylaoluovlollpulpnluzahlukpnlyZahkaalpsCvuipzbukcvuipzdbyklhbmkltuvjobuilihbaluShukzblkspjoklylyzaluZplksbunkplThynhylaoluovlolPPlyypjoalahyjopalravupzjoalpsztpuklydlyapnbukzwlgplssptslagaluIhbhizjoupaapukltOvjoohlbzlynlihbadbykluzvgphswyvislthapzjoShbaZapmabunzlaglukplzlOhlbzlylpuluklbaspjolunlzahsalypzjoluRvuayhzagbyhsaluThynhylaoluovlolBtkplzvgphslualjoupzjolubukhlzaolapzjoluWyvisltlklyThynhylaoluovlolPPgbiloliludbyklilylpazlpuZhuplybunzwyvnyhttilnvuulubtkplvlmmluaspjolDlyazjohlagbunhbjoklyqblunlyluZplksbunzlpuolpaklyThynhylaoluovlolklbaspjogblyovloluKplThynhylaoluovlolPopunlnludbyklbualyKlurthszjobagnlzalssaLpulcvtYboyTbzlbtlpunlypjoalalTbzalydvoubunclynlnludhlyapnakltIlzbjolykplbyzwyblunspjolNlzahsabunklyDvoulpuolpalubukzvsspotkpldvourbsabylsslIlklbabunklzKlurthszThynhylaoluovloltpapoyluchyphisluAfwlunybukypzzluhbjohbzklyPuuluwlyzwlrapclzpjoaihydlyklushzzluGlpadlpzllepzaplyalhbmklyThynhylaoluovlolhbjolpulrslpulRbluzaslyrvsvuplklyluilklbalukzalyNhzaklyMvavnyhmHsilyaYlunlyWhagzjodhyKplzlRvsvupldbyklpuklulyQhoyluhbmnlsvlzaubykplRlyhtprdlyrzahaaThynhylaoluovlollepzaplyauvjoZplpzauhjopukplGljolGvssclylpubtnlgvnluKplkhthspnlNlszlurpyjolulyIlyndlyrzclylpuHNzalssalgbkplzltGdljrhbmlpultGljolunlshluklkpclyzlYhlbtspjorlpalugbyClymblnbunKlyOlpthamvyzjolyObnvYplaodhyJoyvupzaklyNhyaluzahkaThynhylaoluovlolZlpulClyvlmmluaspjobunlupuGlpabunlubukQhoyibljolyuilslnluzlpulmbukplyaluopzavypzjoluZhjorluuaupzzlmblykplpotgbzlpuluSliglpaluLoybunlugbalpsdbykluzvbualyhuklyltklyYolpushukahslybukkhzIbuklzclykpluzarylbgObnvYplaoclymblnalblilylpulbtmhunylpjolIpispvaolrtpaKvrbtlualuHbmglpjoubunlubukdlpalyluopzavypzjoilklbabunzcvssluIlslnluzvdpllpulbtmhunylpjolMvavzhttsbunkpluhjozlpultAvklpuAlpslukltZahkahyjopcLzzluklyIblynlyzjohmaThynhylaoluovlolbukkltLzzlulySbmamhoyahyjopcblilylpnuladvykluzpuk'
    cEntschluesseln(textKappeCry, "H")
    print(ohneSchluessel(textKappeCry))
    
if __name__ == "__main__":
    main()