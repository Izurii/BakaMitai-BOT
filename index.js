require('dotenv').config();

const Discord = require('discord.js');
const discordToken = process.env.DISCORD_TOKEN;
const client = new Discord.Client();
const pythonShell = require('python-shell');
const fs = require('fs-extra');
const configPath = "config\\"
const guildConfigPath = configPath+"guilds\\";

client.on('ready', () => {
	console.log(`Ready!`);
});

client.on('guildCreate', async guild => {

	let defaultGuildConfig = {
		'guildName':guild.name,
		'guildPrefix':'-',
	};

	let filePath = guildConfigPath+guild.id.toString()+'.json';

	fs.writeFile(filePath, JSON.stringify(defaultGuildConfig), function (err) {
		if (err) return console.log(err);
		console.log("'"+guild.name+"' configured.");
	});

});

client.on('message', async message => {

	if(message.author.bot) return;
	var guildPrefix = '';
	var filePath = guildConfigPath+message.guild.id.toString()+'.json';

	fs.readFile(filePath, function(err, data) {
		if (err) return console.log(err);
		let jsonData = JSON.parse(data);
		Object.assign(guildPrefix, jsonData.guildPrefix);
		if(jsonData.guildName!=message.guild.name) {
			jsonData.guildName = message.guild.name;
			fs.writeFile(filePath, JSON.stringify(jsonData), function(err) {
				if (err) return console.log(err);
			});
		}
	});

	if(message.content.startsWith(guildPrefix+'baka')) {
		
		let image = [];
		let processingMessage = message.channel.send("I'm processing the last 20 messages to see if I find some image to do BakaMitai.");
		let messages = await channel.messages.fetch({ limit: 20 });
		messages = Array.from(messages).reverse();
		messages.forEach(function (item, index) {
			if (item[1].embeds.length > 0 || item[1].attachments.size > 0) {
				if (item[1].embeds.length > 0)
					image = item[1].embeds;
				else
					image = item[1].attachments;
				return true;
			}
		});

		let image_url;
		if (image.length == 1) {
			image_url = image[0].thumbnail.url;
		} else if (image.size > 0) {
			let array = Array.from(image);
			array = Array.from(array[0]);
			image_url = array[1].url;
		} else {
			return message.channel.send("I didn't find any image :'(");
		}

		await processingMessage.edit('Processing image...');

	}

});

client.login(discordToken);