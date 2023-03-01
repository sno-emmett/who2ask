#slack ui views

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

def compose_search_results(query):
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
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*nothing*\nI've been folding gliders for years! Ask me anything.\n-<https://acmeco.slack.com/team/U1H63D8SZ|Little Cat>"
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg",
                    "alt_text": "username"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Paper Airplanes*\nI've been folding gliders for years! Ask me anything.\n-<https://acmeco.slack.com/team/U1H63D8SZ|Little Cat>"
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg",
                    "alt_text": "username"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Paper Airplanes*\nI've been folding gliders for years! Ask me anything.\n-<https://acmeco.slack.com/team/U1H63D8SZ|Little Cat>"
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg",
                    "alt_text": "username"
                }
            },
            {
                "type": "divider"
            }
            
        ]
    }
    return view