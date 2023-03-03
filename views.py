#slack ui views
from dbops import *

def compose_home(user_name, user_image):
    view = {
    "type": "home",
	"blocks": [
        {
			"dispatch_action": True,
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"action_id": "input_search",
				"placeholder": {
					"type": "plain_text",
					"text": "[Topic Name]"
				}
			},
			"label": {
				"type": "plain_text",
				"text": ":mag: Search ",
				"emoji": True
			}
		}
	]
    }
    return view

def compose_search_results(query, results):
    results_formatted = [
        {
			"dispatch_action": True,
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"action_id": "input_search",
				"placeholder": {
					"type": "plain_text",
					"text": "[Topic Name]"
				}
			},
			"label": {
				"type": "plain_text",
				"text": ":mag: Search ",
				"emoji": True
			}
		    },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Search results for *{query}:*"
                }
            },
            {
                "type": "divider"
            }
    ]
    
    for result in results[:10]:
        user_id = result[0]
        real_name = result[1]
        avatar = result[2]
        topic_name = result[3].title()
        topic_desc = result[4]
        results_formatted.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{topic_name}*\n{topic_desc}\n:incoming_envelope:<https://snustest.slack.com/team/{user_id}|{real_name}>"
                },
                "accessory": {
                    "type": "image",
                    "image_url": avatar,
                    "alt_text": real_name
                }
        })
        
    results_formatted.append({"type": "divider"})
    
        
    view = {
        "type": "home",
        "blocks": results_formatted
    }
    return view