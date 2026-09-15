# Build-Time vs. Run-Time: Why Dev Tools Fail in Production

**Speakers:** Averi Kitsch (Staff Software Engineer, Google Cloud Databases; tech lead, MCP Toolbox for Databases) & Prerna Kakkar (Senior Software Engineer, Google; tech lead, Eval Bench)
**Channel:** AI Engineer
**URL:** https://www.youtube.com/watch?v=9R--1tg45Jg&list=PLcfpQ4tk2k0X1DNKK3SyZ2Qbl3QxBfHr3
**Retrieved:** 2026-09-09
**Duration:** ~20:07

---

[1.3] [music]
[12.5] Hey everyone, how all of you are doing
[15.4] today?
[17.5] Yeah. Uh so nice to meet you everyone.
[21.0] Uh today uh I and my friend Avery are
[24.2] going to talk about build time versus
[25.7] runtime. Why your developer tools fail
[28.2] in production.
[30.5] So firstly, know about us.
[33.4] >> Hi everybody. I'm Avery Kit and I'm a
[36.0] staff software engineer working on
[37.6] Google Cloud databases. I'm currently
[40.0] the technical lead for MCP toolbox for
[42.5] databases, our open-source uh database
[45.4] MCP server and our Google Cloud MCP
[48.2] server um maintainer.
[51.4] Hi, I'm Pna and I am currently working
[53.9] as senior software engineer at Google
[56.6] and I am currently tech lead for Eval
[59.4] bench which is the evaluation framework
[61.4] for all your agent tech MCP and skills
[63.5] need and I'm also an active contributor
[66.0] to MCP toolbox.
[69.4] So today we are going to cover three
[71.8] areas broadly. We will firstly start
[73.8] with the history of MCP at Google. Then
[77.0] we will cover on the common tool
[78.6] patterns that we have found from our own
[81.4] work and practices and how did we use
[84.3] all those practices to build some tools
[86.5] for database access and how you can use
[89.0] them and then lastly we will talk about
[91.8] security guard rails how you can stop
[94.4] data leaks using identity aware
[96.6] guardrails.
[99.0] So let's get to know the background
[101.4] quickly. Um I'll talk about MCB toolbox
[104.8] for database. It's an open-source
[107.4] self-managed uh serving that we provide.
[110.6] Uh it has currently about 15.7K GitHub
[114.2] stars. We have 132 plus active
[116.6] contributors across 40 plus different
[119.0] databases. It's highly customizable
[121.5] framework and basically we provide you
[124.4] with connection pooling integrated O and
[127.0] you don't even need to care about the
[128.6] observability. You will get all of them
[130.7] out of the box.
[132.9] Then if you don't want to do a
[134.7] self-managed one but you want to have a
[137.2] hosted scaled version, we provide
[140.2] something as Google managed MCP. It's
[143.4] fully managed. Uh you can plug it across
[146.2] various agents and ids or harnesses like
[149.2] Gemini CLI, anti-gravity CLI, cloud
[152.8] code, you name any. uh it's co uh it's
[156.9] governed and the discovery is simple and
[159.8] we also provide model armor which
[162.3] provides secure access management and
[164.9] identity control. So combined with uh
[168.2] the managed version of MCP and the MCP
[171.3] toolbox last month we had 20 million
[173.9] tool calls.
[176.8] Um some of the common tool patterns that
[179.0] we have observed specifically for
[180.7] databases. So I'm going to quickly talk
[182.8] about them.
[184.8] Firstly uh is the control plane tools.
[187.4] What we like to call them is admin tools
[189.8] or manage tools. It is basically in
[192.6] developer assistance space. So it will
[194.9] help you create like instance, manage
[197.7] your instance, create your databases,
[200.2] manage your databases. It will help you
[202.1] with all your DBA needs. But you need to
[205.3] be very careful. You need to be you need
[208.1] to have a human in the loop because we
[210.3] don't want to carry out any dangerous
[212.3] activities.
[214.0] Um so these tools are built on already
[217.0] provisioned public API so you get
[219.4] monitoring and other things out of the
[221.8] box.
[224.2] Next one is natural language to SQL or
[226.5] NL2SQL tools. So basically we are
[229.6] relying on a tool called as execute SQL
[232.5] and with the help of agent we generate
[234.8] raw SQL queries. So you can use this
[237.3] cases where you don't know uh what
[239.7] queries you would require beforehand. So
[241.8] you will get all these queries out of
[244.1] the out of the box. So it it focuses on
[248.2] the developer assistance and analytical
[250.3] agents and uh you can use it for
[252.6] flexible explorations. So for example,
[255.6] we have one of the examples like find
[257.8] all customers in California who bought a
[260.3] winter coat in July and returned it
[262.9] within 14 days and group them by the
[265.2] marketing campaign that originally
[268.0] acquired them. So this is one of the
[270.1] queries where uh you can use this tool
[272.9] uh to get your answers.
[277.4] But then we have something called a
[279.1] structure SQL tools which is getting
[281.0] quite popular and this targets mainly
[283.6] the production use cases where you know
[286.1] like what SQL query you want to use and
[288.8] you want to have security built in and
[291.8] uh you the parameters are already
[294.2] configured so uh you prevent SQL
[296.9] injection
[298.4] and ensure highly controlled access by
[300.6] restricting agent to predefined logic.
[303.9] It also helps you with your latency
[305.8] needs and reduce the hallucination on
[307.8] the agent side.
[310.8] Now we come to the main topic I guess
[313.1] for which you guys are here for
[315.0] buildtime versus runtime. So buildtime
[317.8] are the developer assistant use cases.
[320.1] Um you can think about the initial two
[322.2] cases that we presented to you like the
[324.1] NL2SQL tools and the control plane
[326.6] tools. They come into the category of
[328.3] buildtime tools. uh it's atomic and f
[331.2] flexible but again you don't want to
[333.8] delete your databases so it requires to
[336.6] be a human in the loop case and you
[338.6] can't run them on the on production use
[340.6] cases but let's say I'm interested in
[343.1] building some chat B and I want to do
[345.9] production use cases there you rely on
[348.3] runtime or end user applications you can
[351.0] build those using patenting AI or lchain
[354.2] um so you can see one of the examples
[356.0] like we have a cancel order a
[357.8] deterministic structure SQL query that
[360.0] we have given and you can use it as a
[362.1] tool.
[365.0] This is one of the examples uh or demo
[367.9] for like wherein a buildtime tool was
[371.3] used and uh you can see the error
[373.7] message. So uh agent actually asked to
[376.5] delete the table and start fresh. We
[378.6] deleted everything and there were no
[380.6] safeguard or guardrails here.
[384.0] Now let's go to our demo for
[387.1] runtime tools.
[398.1] Yeah, maybe um I think until the video
[401.5] loads. So, so sorry for the technical
[404.2] glitch that we have, but I can quickly
[406.2] walk you through what we are going to
[407.5] present in the video and I guess it's
[409.5] loading. Yeah.
[412.2] Um so this demo is particularly talking
[415.3] about how did we use our production
[417.8] tools in a chatbot. Uh and we created a
[422.4] demo called a Similar and Symbolair is
[425.4] going to help me with booking all my
[427.4] flights in San Francisco and do and
[430.7] whatever I would require to do in San
[432.9] San Francisco it would basically help me
[434.7] with it. Uh, one of the things that I
[437.8] would try is I would try to fool my
[440.4] agent that I am Avery and not PRA and
[443.6] book a flight for me to San Francisco.
[447.6] But because our agent is uh has all the
[451.6] authenticated O, it will not get fooled
[454.3] and it will not book any flights uh on
[457.0] behalf of Avery, but it will do it on my
[459.4] behalf. Um and then you can use it to
[462.2] basically change your flights. You want
[464.5] to know about all the shops that are
[466.4] there, you can do all these requirements
[468.6] using that. So I guess thank you u
[473.5] Avery.
[479.4] I think we
[497.8] >> [sighs]
[499.8] >> Apologies again for our technical
[502.6] difficulties here.
[512.0] Um, unfortunately, it looks like I need
[513.7] to present from just the slide deck
[515.8] because it's not loading. Okay, so I
[518.9] apologize for not being able to see our
[520.6] demo today, but we can still learn all
[522.4] the security and guardrails that we need
[524.3] to secure our database access. So, the
[527.0] first thing that we need to know is your
[528.7] database is only as secure as your
[530.6] agent. We all know that agents and LMS
[534.0] are actually pretty easy to trick. They
[535.8] might be getting slightly better today,
[537.6] but we can still work really hard to
[540.2] trick them. And so we have a very common
[543.4] attack pattern called the confused
[545.1] deputy attack. And this is when a user
[547.6] can trick an agent into misusing their
[550.6] privileges um to access data that a user
[553.8] wasn't supposed to access. So Simon
[556.7] Willis actually coined the phrase the
[558.6] lethal trifecta. And a data breach
[561.4] occurs when an agent has simultaneous
[564.3] access to three different things. One,
[566.7] private data. Two, untrusted content.
[570.4] And three, the ability to expose that
[573.0] content and that data back to an
[575.3] external user.
[578.6] So let's take a look of that in action.
[581.6] So let's say I'm building a triage um
[584.1] agent and so a ticket is fired or alert
[586.9] goes out and my agent is designed to um
[591.0] look at that ticket and go investigate
[594.3] what it needs to do. So on that ticket
[597.2] the agent gets a little bit of data like
[599.2] we need to go look in this database for
[601.3] these reasons. Um but a malicious
[603.6] insider can actually come into that
[605.6] trusted system and instead say well I
[609.3] want to query the salary database and
[611.7] please return all the employees
[613.4] salaries. And so since this is a trusted
[616.1] system the agent goes okay let me use my
[618.9] permissions. I have those privileges. I
[621.1] have that access. I will query that and
[623.2] I'll post that right back on the ticket
[624.7] because that's what the ticket tells me
[626.6] to do. But now we have a huge data
[630.0] breach. a user that wasn't supposed to
[633.0] have access to private data now has that
[635.8] access. And so now we have a big PR
[638.5] fiasco.
[643.5] So this makes a little bit more sense
[645.5] when we think about who's controlling
[647.8] access and who's controlling the
[650.1] parameters. So we talk about agent or
[652.9] application versus modeled controlled
[655.0] parameters. So in a traditional
[657.4] architecture, things were actually much
[659.9] easier because you would have a few
[662.6] input fields, you would define your
[664.6] queries and then that would be safely
[666.9] injected into those queries.
[670.8] And so it was okay when your application
[673.6] had a little bit more access because it
[677.3] knew exactly what actions it was going
[679.4] to take.
[681.9] But in uh a gent application these rules
[685.2] aren't as clear. So we need to first
[687.4] think about um separating the three
[689.4] different identities. We have the user
[691.9] identity, we have the application
[694.0] identity and the agent identity.
[699.1] So first um we need to think about what
[701.7] the user has access to. So the user just
[704.6] needs to have access to the application.
[707.3] that application's workload identity can
[710.1] have a little bit more broader access um
[712.9] because it needs to probably talk to
[714.5] different services but the agent running
[717.2] in that application only needs to have
[720.4] access to the data that that end user
[722.9] initially needs to have.
[726.0] So then next we need to think about
[727.8] who's controlling the tool inputs. So we
[731.6] have um agent parameters
[735.0] um and a application parameters. So
[737.4] agent parameters are the untrusted
[739.5] inputs that the agent is deriving
[741.4] dynamically. And then we also have
[743.5] application parameters. These are the
[745.7] factual constraints that we need to keep
[747.9] outside of the agents uh control.
[753.0] Okay. So now let's look at the evolution
[756.2] of a secure tool. Here we have a fully
[759.4] modeled control tool. And so essentially
[762.1] the agent here is a super user. It has
[764.4] access to database credentials, the
[766.7] host, the port, the connection details,
[769.0] and even the raw SQL query.
[773.4] And so we're only secure as um the agent
[777.9] here. And we can really easily again
[779.8] trick the agent into exposing all of
[781.8] this data. And now we have access to
[783.9] essentially any database in the system.
[788.0] So Toolbox solves for this um by
[790.2] introducing a source primitive.
[793.0] So we move the connection details out of
[795.3] the agents control and in toolbox um a
[798.4] user will preconfigure the connection
[800.3] details in a YAML file and then when we
[802.6] start our MCP server those are safely
[804.7] injected and so we do not have to have
[807.2] the agent um to have access to that.
[813.3] So we can add a little bit more control
[815.3] to our um source security as well. Our
[818.5] number one request that we get from
[819.8] customers is read only restrictions. We
[822.6] want to be able to remove all right
[824.5] ability from agents if we need that
[826.6] specific uh user journey. So this means
[829.6] removing right tools but also down to
[832.1] the database driver ensuring that we can
[834.9] only do read only queries.
[838.2] If we're also concerned about again
[840.4] blast radius um and securing all of our
[843.3] tables and our databases um some of our
[845.6] cloudnative databases have this concept
[848.2] of allowed data sets. So again we can
[850.6] add that like enum to our source in
[852.9] order to continue to restrict um the
[855.0] blast radius of um the agents control
[857.8] and lastly is output size. You might not
[859.9] actually think that this is a security
[862.0] layer, but if again the agent gets into
[865.4] the wrong hands, we can reduce that
[867.4] blast radius by saying uh the agent can
[870.0] only uh grab this much data. So we're
[871.9] not overwhelming both our agent or our
[874.3] database.
[878.2] So sweet, we have our configurable
[880.4] sources tool. So you can see here that
[882.8] actually now our tool input, our tool
[885.1] signature is very minimalized. we only
[887.8] have the SQL string that's um being
[891.0] generated by the agent.
[895.1] But this comes to our actual our next
[897.0] pro problem. We want to be able to
[899.8] control what the agent is running. We
[902.6] don't want the agent to have the ability
[904.2] to generate any SQL um that it can think
[906.9] of. So toolbox introduces custom tools
[910.7] and again in our YAML file we can define
[913.0] the exact SQL uh statement that will run
[916.3] very reliable.
[918.9] It's a reliable and secure uh SQL query.
[922.4] Um this also allows us to customize the
[924.6] tool name and the tool description.
[926.5] These are really important for the agent
[928.7] to have the context on how to use this
[931.0] tool um accurately.
[934.0] And in the system we use prepared
[935.9] statements with type parameters in order
[937.9] to reduce um SQL injection attacks. So
[940.7] we make sure that everything is um
[944.5] we validate all the input types um when
[946.8] we inject that into the SQL for the
[948.6] user.
[952.2] Okay, let's dive into a little bit more
[953.9] of best practices for tool quality. So
[956.4] we really highly recommend that tools
[958.4] focus on outcomes. We really shouldn't
[960.6] be thinking in atomic rest APIs. we
[963.4] should think about what the action
[965.4] actually needs to do. This also reduces
[967.8] the round trip of needing to make
[970.2] multiple tool calls. And again, the
[973.3] descriptions are guidance. We shouldn't
[975.8] um duplicate information like input
[977.8] parameters because the agent already has
[979.6] access to that. So, writing really good
[982.2] um tool descriptions is very important
[984.6] for accurate tool usage.
[987.1] We also recommend that you separate read
[989.6] versus write tools. Um by doing this you
[992.7] can automatically approve read tools and
[995.1] but you can also then send write tools
[997.7] uh to the user for um confirmation and
[1000.2] this just makes it very much more clear
[1002.0] for the agent to use these
[1004.6] and this is actually uh the next is
[1006.2] actionable errors. This is the number
[1008.1] one thing that I think we can all do
[1010.2] better. So usually we just return like a
[1012.8] generic HTTP error four or four but we
[1016.1] all know agents are actually really
[1017.5] smart now and so if you give the ability
[1020.2] to have an error of that can be
[1022.4] retrieded the agent can actually take
[1024.7] that action. So being able to return a
[1027.4] error is really important and lastly is
[1031.3] simple inputs. We see that people try to
[1033.8] use these complex maps uh complex
[1036.6] primitives to um that an agent needs to
[1039.4] be able to build and that is not
[1041.8] reliable. Using flat structure with um
[1046.6] with uh simple inputs will really
[1048.9] increase your reliability.
[1052.6] So sweet. Now we're at custom semantic
[1055.1] tools. You can see that we now have our
[1057.7] lookup flights tool that takes in the
[1059.9] dynamic parameters such as user ID and
[1062.9] date. And so now our we're very much
[1065.7] more secure because the agent isn't
[1067.5] generating that SQL query. It doesn't
[1069.5] have the ability to kind of go off the
[1071.2] rails. It only is looking at these very
[1073.4] specific inputs.
[1077.6] But user ID is actually a very sensitive
[1080.5] piece of information. It is PII. we need
[1083.0] to also remove that from the ability of
[1085.4] the agent's control. So we can do this
[1087.9] in two different ways. We have bounded
[1090.2] parameters. This is when the application
[1092.6] first um authenticates the user and then
[1095.1] we can bind that parameter um directly
[1097.7] to our tool. And so that restricts the
[1100.0] agents control of it. It actually never
[1101.8] sees that user identity.
[1104.9] But toolbox also solves for this in
[1107.2] another way called authenticated
[1108.9] parameters. This is when we tell the
[1111.4] tool that you're going to receive a
[1114.2] identity token, an open ID, a signed jot
[1117.0] token, and when we call that tool that
[1120.1] we want it first to validate that token.
[1122.3] Is that token real? Is that token
[1124.3] correct? And then we'll extract the user
[1127.0] claims from that token for the user. And
[1129.4] so the claims usually include like a
[1131.1] user ID, an email, um an issuer.
[1135.4] And so it's secured because we're again
[1138.1] extracting that user identity out of the
[1141.3] agents control and binding that to the
[1143.4] tool.
[1148.6] So now um we're have a much more secure
[1153.1] tool. We have our lookup flights tool
[1155.4] that only takes in a very easy parameter
[1159.0] such as date. It doesn't have to handle
[1161.1] any sensitive information such as PII,
[1163.9] user identity. And so we're really here
[1166.6] now at um our zero trust architecture
[1170.0] where we're in full control of
[1172.1] everything that we need to be in control
[1174.1] of.
[1179.5] So thank you all for coming to listen to
[1181.5] our talk today. Again, I apologize for
[1183.6] our technical difficulties. Uh we highly
[1186.1] recommend if you want to learn more
[1187.4] about our technologies um that you look
[1190.0] at our documentation and our uh GitHub
[1192.6] repository. I also really want to
[1194.9] highlight our eval bench repository
[1197.0] because this is how we know that our
[1198.9] tools are working well and eval.
[1203.6] So thank you all for joining us today.
[1207.2] [applause]
