#slack ui views
from dbops import *

def compose_home(user_name, user_image, is_admin):
    # if not is_admin:
    view = {
        "type": "home",
        "blocks": [
            {
			"type": "actions",
			"elements": [
				{
					"type": "button",
                    "action_id": "button_view_profile",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "View Profile"
					},
					"value": "View Profile",
				}
			]
		    },
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

def compose_search_results(query, results, is_admin):
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

def compose_profile(topics):
    #print(topics)
    topics_formatted = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Your Topics*"
			}
		},
		{
			"type": "actions",
			"elements": [
                {
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Return to Search"
					},
					"value": "click_me_123"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Add Topic"
					},
					"style": "primary",
					"value": "click_me_123"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Delete Topic"
					},
					"style": "danger",
					"value": "click_me_123"
				}
			]
		},
		{
			"type": "divider"
		}
    ]
    
    for topic in topics:
        topic_title = topic[1]
        topic_notes = topic[2]
        topic_badge_community = topic[3]
        topic_badge_snohetta = topic[4]
        topics_formatted.append({
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*{topic_title}*\n{topic_notes}"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"emoji": True,
					"text": "Edit"
				},
				"value": "click_me_123"
			}
		})
	
    topics_formatted.append({"type": "divider"})
    
    view = {
        "type": "home",
        "blocks": topics_formatted
    }
    return view