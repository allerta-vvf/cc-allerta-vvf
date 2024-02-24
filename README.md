# AllertaVVF integration plugin for Cheshire Cat

Using this plugin, you can use Cheshire Cat to use the AllertaVVF platform, allowing the cat to read and update availability, send alerts, read and summarize services data and more.

![AllertaVVF](./logo.png)

## Usage

1. Install the plugin
2. Go to settings and set the AllertaVVF credentials (API Token and API endpoint URL)
3. Use the cat to read and update availability, send alerts, read and summarize services data and more.

### Notice

This is not production ready yet, use at your own risk.

### How to obtain the API Token

To obtain the API Token, you need to make an http POST request to the login endpoint of the AllertaVVF platform, providing your username and password.  
You can use the following curl command to obtain the token:

```bash
curl -X POST "ALLERTA_URL/api/login" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"username\":\"your_username\",\"password\":\"your_password\"}"
```

The response will be a JSON object containing the token, like this
    
```json
{
"access_token":"1|RANDOMDATAHERE",
"token_type":"Bearer",
"auth_type":"token"
}
```

You can then use the `access_token` as the API Token in the plugin settings.  
Remember to copy anything (not just the part after the `|` character), and to keep it secret.

## Installing AllertaVVF

You can install the AllertaVVF platform by following the instructions on the [official website](https://allerta-vvf.github.io/docs/getting-started).
