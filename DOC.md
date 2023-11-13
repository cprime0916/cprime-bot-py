# C'Bot

<p>This bot is designed for the smspt server, the commands can be divided into several categories. <br> Note that this project is still in early development stage, so this markdown file may not be accurate 
over time <br>
<br> Credits to tkt for reference in <tt>contests_fn.py</tt> and the contests commands.</p>

## Linking

### <tt>.link</tt>

#### Syntax
<p><tt>.link [cfUser]</tt> <br> </p>

#### Description
<p><tt>v1.0</tt> <br> This command links [cfUser] to your discord account. <br> When [cfUser] is an exisiting handle in codeforces, the bot will send a green embed message. <br> Otherwise, it
will send a red error embed message.</p>

#### Examples
<p><tt>.link omega0916</tt></p>

<hr>

### <tt>.unlink</tt>

#### Syntax
<p><tt>.unlink user [cfUser]</tt></p>
<p><tt>.unlink all</tt></p>

#### Description
<p><tt>v1.0</tt> <br> This command unlinks all the previous linked accounts with the <tt>all</tt> parameter provided.</p> <p><tt>dbg</tt> <br> If <tt>user</tt> and <tt>[cfUser]</tt> is provided instead, the bot will check if <tt>[cfUser]</tt> is linked. <br> If it is, then
the bot will send a green embed message. <br> Otherwise, it will send a red error embed message.</p>


## Contests

### <tt>.contests</tt>

#### Description
<p><tt>v1.0</tt> <br> This command makes the bot send all the contests in codeforces and atcoder. </p>
<hr>
Work in progress...
