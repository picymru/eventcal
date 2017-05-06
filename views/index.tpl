% include('global/header.tpl')
<section class="hero">
	<div class="container">
			<h1>Events</h1>
	</div>
</section>

<section id="content" class="content">
	<div class="container">
		<div class="onecolumn">
			% for event in events:
				<h2>{{event['title']}}</h2>
				<div class="blog-item">
					<h6 class="date"><span class="icon-calendar"></span>{{event['date']}}</h6>              
					<p>{{event['desc']}}</p>
					<a href="./events/{{event['id']}}">View event page &raquo;</a>
				</div>
			% end
		</div>
	</div>
% include('global/footer.tpl')