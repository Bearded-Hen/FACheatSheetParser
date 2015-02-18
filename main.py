__author__ = 'jamielynch'

if __name__ == "__main__":
    import parser
    import datetime

    map = parser.parseFaCheatSheet()

    file = open("out.txt", "w")
    file.write("\n// Auto-generated FA-Map from " + datetime.date.today().strftime("%Y-%m-%d") + "\n\n")

    for k, v in sorted(map.iteritems()):
        mapEntry = "faMap.put(\"{key}\", \"{value}\");\n".format(key=k, value=v)
        file.write(mapEntry)