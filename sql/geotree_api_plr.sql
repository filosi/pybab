------------------
-- PREREQUSITES --
------------------
CREATE EXTENSION IF NOT EXISTS plr;
SELECT * FROM plr_set_display(':5.0'); -- IMPORTANTE!!! Altrimenti R non trova il DISPLAY!

--------------------------
--- PRINTING FUNCTIONS ---
--------------------------
DROP FUNCTION IF EXISTS gt_print (bigint[], bigint[], text[], double precision[]);
CREATE OR REPLACE FUNCTION gt_print (bigint[], bigint[], text[], double precision[])
RETURNS VOID AS '
	edges=c() 
	library(igraph)

	for( i in 1:length(arg1))
		{
			edges[2*i-1]=arg1[i]
			edges[2*i]=arg2[i]
		}
	g<-graph(edges=edges,directed=T)
	V(g)$label=arg3
	V(g)$color[which(arg4==6.0)]=''red''
	V(g)$color[which(arg4==5.0)]=''blue''
	V(g)$color[which(arg4==7.0)]=''green''
	png("grafo.png",height=1920,width=1920)
	plot(g,layout=layout.fruchterman.reingold,
		vertex.size=2,vertex.label.degree=0,vertex.label.dist=0.2,
		edge.arrow.size=0.4,edge.width=0.4,edge.color=''black'')
	dev.off()
' LANGUAGE 'plr' STRICT;

/*select gt_print(
	(select array(select gt_element_id from gt_tree order by id)),
	(select array(select gt_parent_id from gt_tree order by id)),
	(select array(select name from gt_element where id >= 0 order by id)),
	(select array(select rank from gt_element where id >= 0 order by id))
);*/

DROP FUNCTION IF EXISTS gt_print (bigint[], bigint[]);
CREATE OR REPLACE FUNCTION gt_print (bigint[], bigint[])
RETURNS VOID AS '
	edges=c() 
	library(igraph)

	for( i in 1:length(arg1))
		{
			edges[2*i-1]=arg1[i]
			edges[2*i]=arg2[i]
		}
	g<-graph(edges=edges,directed=T)
	png("grafo.pdf")
	plot(g)
	dev.off()
' LANGUAGE 'plr' STRICT;

drop function if exists r_plot_heat_logistic(integer,integer);
create or replace function r_plot_heat_logistic(width integer, height integer) returns char[] as $$
    ## necessary libraries
    require(cairoDevice)
    require(RGtk2)

   # width <- 1000
   # height <- 1000

    ## create colormap and plotting device
    pixmap <- gdkPixmapNew(w=width, h=height, depth=24)
    asCairoDevice(pixmap)

    ## get data
    x <- seq(0,6.28,0.01)
    myplot = plot(x,sin(x),type='l')
    print(myplot)

    plotPixbuf <- gdkPixbufGetFromDrawable(NULL, pixmap, pixmap$getColormap(), 0, 0, 0, 0, width, height)
    buffer <- gdkPixbufSaveToBufferv(plotPixbuf, 'png', character(0), character(0))$buffer
    dev.off()
    return(buffer)
$$ language plr;

drop function if exists r_plot_heat_logistic_bytea(integer,integer);
create or replace function r_plot_heat_logistic_bytea(width integer, height integer) returns bytea as $$
    ## necessary libraries
    require(cairoDevice)
    require(RGtk2)

    ## create colormap and plotting device
    pixmap <- gdkPixmapNew(w=width, h=height, depth=24)
    asCairoDevice(pixmap)

    ## get data
    x <- seq(0,6.28,0.01)
    myplot = plot(x,sin(x),type='l')
    print(myplot)

    plotPixbuf <- gdkPixbufGetFromDrawable(NULL, pixmap, pixmap$getColormap(), 0, 0, 0, 0, width, height)
    buffer <- gdkPixbufSaveToBufferv(plotPixbuf, 'png', character(0), character(0))$buffer
    dev.off()
    return(buffer)
$$ language plr;

create function r_plot_heat_logistic(r_from numeric, r_to numeric, width integer, height integer) returns bytea as $$
    ## uses plr functions r_logistic_set() and r_logistic()
    ## function to make jpeg as bytea to hand out of database
    ## Uses RColorBrewer to make nice color paletter
    ## and lattice to make levelplot
    ## try width = 1600 and height = 1200

    ## necessary libraries
    require(lattice)
    require(cairoDevice)
    require(RColorBrewer)
    require(RGtk2)


    ## create colormap and plotting device
    mycuts = 11
    mypal = brewer.pal(mycuts, 'Spectral')
    pixmap <- gdkPixmapNew(w=width, h=height, depth=24)
    asCairoDevice(pixmap)

    ## get data
    my.qry = sprintf("select * from test_logistic where r between %s and %s;", r_from, r_to)
    tmp = dbGetQuery('', my.qry)
    tmp$index = as.Date(tmp$index)

    ## plot data
    myplot = levelplot( x ~ index *r, data=tmp,
            col.regions=mypal, cuts=(mycuts-1)
    )


    print(myplot)
    plotPixbuf <- gdkPixbufGetFromDrawable(NULL, pixmap, # 0, 0, 0, 0, width, height)
               pixmap$getColormap(), 0, 0, 0, 0, width, height)
    buffer <- gdkPixbufSaveToBufferv(plotPixbuf, 'png', character(0), character(0))$buffer
    return(buffer)
$$ language plr;

select * from r_plot_heat_logistic(1000,1000);

select * from unnest(r_plot_heat_logistic(2000,2000));
select * from array_length(r_plot_heat_logistic(2000,2000),1);

select * from array_to_string(r_plot_heat_logistic(2000,2000),'');
select * from length(array_to_string(r_plot_heat_logistic(2000,2000),''));

select * from decode(array_to_string(r_plot_heat_logistic(2000,2000),''),'hex');
select * from length(decode(array_to_string(r_plot_heat_logistic(2000,2000),''),'hex'));

select * from plr_environ() order by name


/*select gt_print(
	(select array(select gt_element_id from gt_tree order by id)),
	(select array(select gt_parent_id from gt_tree order by id))
);*/
