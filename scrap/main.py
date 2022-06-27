
import crawler
import options

if __name__ == "__main__":
    
    opt = options.parser.parse_args()
    temp_crawler = crawler.Crawler(opt)
    temp_crawler.Search("이슬람", opt)
    temp_crawler.pages()
    

