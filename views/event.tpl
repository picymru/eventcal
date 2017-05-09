% include('global/header.tpl')
<section class="hero">
	<div class="container">
			<h1>{{event['title']}}</h1>
	</div>
</section>

<section id="content" class="content">
	<div class="container">
		<div class="onecolumn">
			<div class="blog-item full">
				<h6 class="date">
					<span class="icon-calendar"></span>{{event['date']}}
					
					% if event['time'] != "00:00" and event['timeEnd'] != "00:00":
					 {{event['time']}}
					% elif event['date'] != event['dateEnd']:
					 - {{event['dateEnd']}}
					% end

					% if event['time'] != event['timeEnd']:
					 - {{event['timeEnd']}}
					% end
					<br />
					% if event['location'] != '':
						<span class="icon-pushpin"></span>{{event['location']}} <a href="http://maps.google.com/?q={{event['location']}}">[map]</a>
					% end
				</h6>
				{{!event['desc']}}
				% if event['url'] != '':
					<a class="read-more" href="{{event['url']}}" target="_blank">
						Book tickets, or find out more &raquo;
					</a>
				% end
			</div>
		</div>
	</div>
</section>
% include('global/footer.tpl')