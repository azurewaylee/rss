import xml.etree.ElementTree as ET


def load_opml(opml_path):
    tree = ET.parse(opml_path)
    root = tree.getroot()

    outlines = root.findall(".//outline[@xmlUrl]")

    feeds = []

    for outline in outlines:
        feeds.append({
            "title": outline.attrib.get("title")
                     or outline.attrib.get("text")
                     or "(无标题)",
            "url": outline.attrib.get("xmlUrl")
        })

    return feeds