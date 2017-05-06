% include('global/header.tpl')
<section class="hero">
	<div class="container">
			<h1>{{event['title']}}</h1>
	</div>
</section>

<section id="content" class="content">
	<div class="container">
		<div class="onecolumn">
			<div class="blog-item">
				<h6 class="date">
					<span class="icon-calendar"></span>{{event['date']}}<br />
					<span class="icon-pushpin"></span>{{event['location']}} <a href="http://maps.google.com/?q={{event['location']}}">[map]</a>
				</h6>
				{{!event['desc']}}
				<a href="{{event['url']}}">Book tickets, or find out more &raquo;</a>
			</div>
		</div>
	</div>
</section>
% include('global/footer.tpl')