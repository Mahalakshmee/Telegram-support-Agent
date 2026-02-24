const fs = require("fs");
const { google } = require("googleapis");
const readline = require("readline");

const SCOPES = ["https://www.googleapis.com/auth/gmail.send"];
const CREDENTIALS_PATH = "gmail_credentials.json";
const TOKEN_PATH = "token_email.json";

const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH));
const { client_id, client_secret, redirect_uris } = credentials.web;

const oAuth2Client = new google.auth.OAuth2(
  client_id,
  client_secret,
  redirect_uris[0]
);

async function generateToken() {
  const authUrl = oAuth2Client.generateAuthUrl({
    access_type: "offline",
    scope: SCOPES,
    prompt: "consent"
  });

  console.log("Authorize this app by visiting:\n", authUrl);

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  rl.question("Enter the code from browser: ", async (code) => {
    rl.close();
    const { tokens } = await oAuth2Client.getToken(code);
    fs.writeFileSync(TOKEN_PATH, JSON.stringify(tokens, null, 2));
    console.log("✅ Gmail token generated: token_email.json");
  });
}

generateToken();
