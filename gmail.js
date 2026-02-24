const nodemailer = require("nodemailer");
const config = require("./config");
const { google } = require("googleapis");

const OAuth2 = google.auth.OAuth2;
const oauth2Client = new OAuth2(
  config.clientId,
  config.clientSecret,
  "https://developers.google.com/oauthplayground"
);

oauth2Client.setCredentials({
  refresh_token: config.refreshToken
});

const input = process.argv[2];
const data = JSON.parse(input);
const productName = data.productName;
const finalPrice = data.finalPrice;

async function sendMail(productName, finalPrice) {
  try {
    const accessTokenResponse = await oauth2Client.getAccessToken();
    const accessToken = accessTokenResponse.token;

    const transporter = nodemailer.createTransport({
      service: "gmail",
      auth: {
        type: "OAuth2",
        user: config.emailUser,
        clientId: config.clientId,
        clientSecret: config.clientSecret,
        refreshToken: config.refreshToken,
        accessToken: accessToken
      }
    });

    const mailOptions = {
      subject: `🎉 Congratulations! Your purchase of ${productName} is confirmed`,
      to: "mahabaskaran50@gmail.com",
      text: `Hi there,

Thank you for purchasing "${productName}" from our store!

The final price for your order is: ₹${finalPrice}.

We appreciate your business and hope you enjoy your new product!

Best regards,
Support Team`
    };

    const result = await transporter.sendMail(mailOptions);
    console.log("✅ Email sent:", result.response);

  } catch (error) {
    console.error("❌ Error sending email:", error);
  }
}
sendMail(productName, finalPrice);
