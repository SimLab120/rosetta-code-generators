import zipfile
from lxml import etree

def parse_lucidchart_bpmn_vsdx(vsdx_file_path):
    """
    Parses a Lucidchart-exported BPMN process map from a .vsdx (Visio) file.
    Returns a dictionary with tasks, events, gateways, annotations, and data objects.
    """
    # Namespace mappings
    ns = {
        'visio': 'http://schemas.microsoft.com/office/visio/2012/main',
        'lc': 'http://www.lucidchart.com'
    }

    # Open the vsdx file as a zip and find the page XMLs
    with zipfile.ZipFile(vsdx_file_path) as z:
        # Find all page xmls (e.g., 'visio/pages/page1.xml')
        page_files = [f for f in z.namelist() if f.lower().startswith('visio/pages/page') and f.lower().endswith('.xml')]
        bpmn_elements = {
            "tasks": [],
            "events": [],
            "gateways": [],
            "annotations": [],
            "data_objects": [],
            "connections": []
        }

        for page_file in page_files:
            xml_data = z.read(page_file)
            root = etree.fromstring(xml_data)

            for shape in root.findall('.//visio:Shape', namespaces=ns):
                nameU = shape.get('NameU', '')
                name = shape.get('Name', '')
                element = None

                # -------- Tasks --------
                if nameU.startswith('com.lucidchart.BPMNActivity'):
                    # Task type: lc:Property[@Name="bpmnActivityType"], Task name: <Text>
                    task_type = None
                    task_type_elem = shape.find('lc:Property[@Name="bpmnActivityType"]', namespaces=ns)
                    if task_type_elem is not None:
                        task_type = task_type_elem.text
                    task_name = ''
                    text_elem = shape.find('visio:Text', namespaces=ns)
                    if text_elem is not None:
                        task_name = ''.join(text_elem.itertext()).strip()
                    element = {
                        "id": shape.get("ID"),
                        "task_type": task_type,
                        "task_name": task_name
                    }
                    bpmn_elements["tasks"].append(element)

                # -------- Events --------
                elif nameU.startswith('com.lucidchart.BPMNEvent'):
                    # Event type: lc:Property[@Name="bpmnEventType"], group: lc:Property[@Name="bpmnEventGroup"], name: <Text>
                    event_type = None
                    event_group = None
                    event_type_elem = shape.find('lc:Property[@Name="bpmnEventType"]', namespaces=ns)
                    if event_type_elem is not None:
                        event_type = event_type_elem.text
                    event_group_elem = shape.find('lc:Property[@Name="bpmnEventGroup"]', namespaces=ns)
                    if event_group_elem is not None:
                        event_group = event_group_elem.text
                    event_name = ''
                    text_elem = shape.find('visio:Text', namespaces=ns)
                    if text_elem is not None:
                        event_name = ''.join(text_elem.itertext()).strip()
                    element = {
                        "id": shape.get("ID"),
                        "event_type": event_type,
                        "event_group": event_group,
                        "event_name": event_name
                    }
                    bpmn_elements["events"].append(element)

                # -------- Gateways --------
                elif nameU.startswith('com.lucidchart.BPMNGateway'):
                    # Gateway type: lc:Property[@Name="bpmnGatewayType"], name: <Text>
                    gateway_type = None
                    gateway_type_elem = shape.find('lc:Property[@Name="bpmnGatewayType"]', namespaces=ns)
                    if gateway_type_elem is not None:
                        gateway_type = gateway_type_elem.text
                    gateway_name = ''
                    text_elem = shape.find('visio:Text', namespaces=ns)
                    if text_elem is not None:
                        gateway_name = ''.join(text_elem.itertext()).strip()
                    element = {
                        "id": shape.get("ID"),
                        "gateway_type": gateway_type,
                        "gateway_name": gateway_name
                    }
                    bpmn_elements["gateways"].append(element)

                # -------- Annotations --------
                elif nameU.startswith('com.lucidchart.BPMNTextAnnotation'):
                    # Annotation text: <Text>
                    annotation_text = ''
                    text_elem = shape.find('visio:Text', namespaces=ns)
                    if text_elem is not None:
                        annotation_text = ''.join(text_elem.itertext()).strip()
                    element = {
                        "id": shape.get("ID"),
                        "annotation_text": annotation_text
                    }
                    bpmn_elements["annotations"].append(element)

                # -------- Data Objects --------
                elif nameU.startswith('com.lucidchart.BPMNData'):
                    # Data type: lc:Property[@Name="bpmnDataType"], name: <Text>
                    data_type = None
                    data_type_elem = shape.find('lc:Property[@Name="bpmnDataType"]', namespaces=ns)
                    if data_type_elem is not None:
                        data_type = data_type_elem.text
                    data_name = ''
                    text_elem = shape.find('visio:Text', namespaces=ns)
                    if text_elem is not None:
                        data_name = ''.join(text_elem.itertext()).strip()
                    element = {
                        "id": shape.get("ID"),
                        "data_type": data_type,
                        "data_name": data_name
                    }
                    bpmn_elements["data_objects"].append(element)

                

        return bpmn_elements
    

result = parse_lucidchart_bpmn_vsdx('Sample.vsdx')
# print(result['tasks'])
# print(result['events'])