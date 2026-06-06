# honey_runtime.py
# High-performance embeddable interdiction script runtime simulation.
from pathlib import Path
class HoneyModule:
    def __init__(self, script_content: str):
        self.script_content = script_content
        
    def mask_payload(self, payload: str) -> dict:
        state_dict = {}
        url_counter = 0
        coord_counter = 0
        
        masked_text = []
        i = 0
        n = len(payload)
        
        while i < n:
            byte = payload[i]
            
            # Fast-path URL extraction
            if byte == 'h' and payload[i:i+4] == "http":
                url_end = i
                while url_end < n and not payload[url_end].isspace():
                    url_end += 1
                target_url = payload[i:url_end]
                
                url_counter += 1
                placeholder = f"__URL_ENTITY_{url_counter:03d}__"
                state_dict[placeholder] = target_url
                masked_text.append(placeholder)
                
                i = url_end
                continue
                
            # Spatial Coordinate Extraction
            if byte == '-' and i + 1 < n and payload[i+1].isdigit():
                coord_end = i + 1
                while coord_end < n and (payload[coord_end].isdigit() or payload[coord_end] == '.'):
                    coord_end += 1
                target_coord = payload[i:coord_end]
                
                coord_counter += 1
                placeholder = f"__COORD_ENTITY_{coord_counter:03d}__"
                state_dict[placeholder] = target_coord
                masked_text.append(placeholder)
                
                i = coord_end
                continue
                
            masked_text.append(byte)
            i += 1
            
        masked_str = "".join(masked_text)
        return {
            "masked_text": masked_str,
            "ledger": state_dict
        }
        
    def demask_payload(self, generated_text: str, state_dict: dict) -> str:
        final_output = generated_text
        for key, val in state_dict.items():
            final_output = final_output.replace(key, val)
        return final_output
def load_script(path: str) -> HoneyModule:
    content = Path(path).read_text(encoding="utf-8")
    return HoneyModule(content)
