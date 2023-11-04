# C'Bot

<p>This bot is designed for the smspt server, the commands can be divided into several categories. <br> Note that this project is still in early development stage, so this markdown file may not be accurate 
over time <br>
<br> Credits to tkt for reference in <tt>contests_fn.py</tt> and the contests commands.</p>

## Linking

### <tt>.link</tt>

#### Format
<p><tt>.link [cfUser]</tt> <br> </p>

#### Description
<p><tt>v1.0</tt> <br> This command links [cfUser] to your discord account. <br> When [cfUser] is an exisiting handle in codeforces, the bot will send a green embed message. <br> Otherwise, it
will send a red error embed message.</p>

#### Examples
<p><tt>.link omega0916</tt></p>

<hr>

### <tt>.unlink</tt>

#### Format
<p><tt>.unlink [cfUser]</tt></p>
<p><tt>.unlink</tt></p>

#### Description
<p><tt>cid</tt> <br> This command unlinks all the previous linked accounts with no [cfUser] provided. <br> If [cfUser] is provided, the bot will check if [cfUser] is linked. <br> If it is, then
the bot will send a green embed message. <br> Otherwise, it will send a red error embed message.</p>

<hr>

Work in progress...
