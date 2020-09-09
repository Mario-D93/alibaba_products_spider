# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class EarphonesSpider(scrapy.Spider):
    name = 'earphones'
    allowed_domains = ['alibaba.com']

    script = '''
    function main(splash, args)
        splash.private_mode_enabled = false
        assert(splash:go(args.url))
        assert(splash:wait(2))
        
        minprice_btn = splash:select('.price-between:first-of-type')
        minprice_btn:mouse_click()
        minprice_btn:send_text('100')
        assert(splash:wait(0.5))
        btn_1 = splash:select('.price-between-ok')
        btn_1:mouse_click()
        assert(splash:wait(2))
  			
  		minorder_btn = splash:select('.min-order-input')
        minorder_btn:mouse_click()
        minorder_btn:send_text('40')
        assert(splash:wait(0.5))
        btn_2 = splash:select('.min-order-ok')
        btn_2:mouse_click()
        assert(splash:wait(2))

        return {
            html = splash:html(),
        }
    end
    '''

    script_next_page = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(2))
            
            splash:set_viewport_full()
            assert(splash:wait(2))
            return {
                html = splash:html(),
            }
        end
    '''

    def start_requests(self):
        yield SplashRequest(url='https://www.alibaba.com/catalogs/products/CID205791204?spm=a27aq.13817715.hot_categories.4.e8d671a9wOQdBS&SearchScene=cps&IndexArea=product_en',
            callback=self.parse, endpoint='execute', args={'lua_source':self.script})
        

    def parse(self, response):

        print(response)
        products = response.xpath("//div[@class='m-gallery-product-item-wrap']")
        for item in products:
            title = item.xpath("normalize-space(.//div/div/div[@class='item-info']/h2/a/text())").get()
            #url = 'https:'+item.xpath(".//div/div/div[@class='item-info']/h2/a/@href").get()
            price = item.xpath("normalize-space(.//div[@class='pmo']/div[@class='price']/b/text())").get()
            qty = item.xpath(".//div[@class='pmo']/div[@class='min-order']/b/text()").get()
            
            yield{
                'product_title': title,
                #'product_url':url,
                'price':price,
                'min_order_qty':qty,
                'url':response.url,

            }

        next_page = 'https:'+response.xpath("//span[@class='current']/following-sibling::a[1]/@href").get()
        

        if len(products) == 40:
            if next_page:
                yield SplashRequest(url=next_page,
                    callback=self.parse, endpoint='execute', args={'lua_source':self.script_next_page })
            
            

