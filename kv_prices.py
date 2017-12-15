#!/usr/bin/python3
import psycopg2, sys, requests, time, random
import xml.etree.ElementTree as ET

info_query = 'insert into object_info(object_id, address, description_text, description, price, pic_url, obj_url) values (%s,%s,%s,%s,%s,%s,%s);'

# make xml parser shut up
magic = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd" [
<!ENTITY nbsp ' '>
]>'''
apartment_codes = 'http://kinnisvaraportaal-kv-ee.postimees.ee/?act=search.objectcoords&last_deal_type=1&company_id=&page=1&orderby=ob&page_size=60&deal_type=1&dt_select=1&county=1&parish=421&rooms_min=1&rooms_max=3&price_min=40000&price_max=70000&nr_of_people=&area_min=&area_max=&keyword=&fuseaction=search.objectcoords&cluster=0&search_id=0&object_type=1&price=&price_m2_min=0&price_m2_max=0&change_interest=0&price_type=1&price_field=price_eur&area_total_min=&area_total_max=&area_ground_min=&area_ground_max=&not_last=&images_only=0&videos_only=0&date_created=&date_activated=&ad_home_page=0&broker_id=&coords=&owner_agreement=&name_first=&name_last=&bid_objects=0&energy_cert=&energy_cert_val=&date_deal_success=0&coop_only=0&raise_obj=&country_id=1&recent=0&start_coordinates=&distance=0&detail_plan=&start=1&withlimit=0&debug=&lng=&cluster=true&nelat=59.457500247589344&nelng=24.849574350740795&swlat=59.39638098131991&swlng=24.64049079361189&zoom=100'
apartment_detail = 'http://kinnisvaraportaal-kv-ee.postimees.ee/?act=search.objectinfo&object_id='
conn_string = "host='localhost' dbname='kv_prices' user='USER HERE' password='PASSWORD HERE'"

def main():

    print("Connecting to database...")
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print("Connected!\n")

    apartments = requests.get(apartment_codes)
    if apartments.status_code == 200:
        data = apartments.json()
        print("Got {} apartments".format(data["total"]))
        insert_values = ""
        for apartment in data["markers"]:
            # validate input
            try:
                float(apartment["0"])
                float(apartment["1"])
                float(apartment["object_id"])
            except:
                print("Incorrect element: " + str(apartment))
                continue
            insert_values += "({0},{1},{2}),".format(apartment["0"], apartment["1"], apartment["object_id"])
        apartment_list = [apartment["object_id"] for apartment in data["markers"]]
        check_string = "select object_id from objects;"
        cursor.execute(check_string)
        existing_apartments = [apartment[0] for apartment in cursor.fetchall()]
        print(existing_apartments)
        new_apartments = [apartment for apartment in apartment_list if apartment not in existing_apartments]
        #print(new_apartments)
        if new_apartments:
            print("NEW APARTMENTS: " + str(new_apartments))
            try:
                # write new apartments in a local file so it can easily be picked up and flushed
                with open("new_ap.txt", "a") as f:
                    f.write("\n".join(new_apartments))
                    f.write("\n")
            except Exception as e:
                print("Failed to write new apartments.")
                print(e)
        insert_string = "insert into objects(x, y, object_id) values " + insert_values[:-1] + " on conflict do nothing;"
        print(insert_string)
        cursor.execute(insert_string)
        conn.commit()
        print("Inserted new rows")
        i = 0
        for apartment in data["markers"]:
            apartment_info = requests.get(apartment_detail + apartment["object_id"])
            if apartment_info.status_code == 200:
                # some cleanup
                html = apartment_info.text.replace('<span class="sep">|</span>', ' ').replace('&nbsp;', ' ').replace('\xa0', ' ').replace('<strong>', '').replace('</strong>', '')
                # print(html)
                tree = ET.fromstring(magic + html)

                image = None
                link = None
                headline = None
                price = None
                description_text = None
                description = None

                imgs = tree.findall("p[@class='object-photo']/a/img")
                if imgs:
                    image = imgs[0].attrib["src"]

                links = tree.findall("p[@class='object-photo']/a")
                if links:
                    link = links[0].attrib["href"]

                titles = tree.findall("h2[@class='object-title']/a")
                if titles:
                    headline = titles[0].text

                prices = tree.findall("div/p")
                #does not work: prices = tree.findall('p[@class="object-price"]')
                for price in prices:
                    if '€' in price.text:
                        price = price.text.replace('€', '').replace(' ', '')
                        break

                notes = tree.findall("p[@class='object-important-note']")
                if notes:
                    description_text = notes[0].text

                metas = tree.findall("p[@class='object-meta']")
                if metas:
                    description = metas[0].text

                print((apartment["object_id"], headline, description_text, description, price, image, link))
                cursor.execute(info_query, (apartment["object_id"], headline, description_text, description, price, image, link))

                # commit the changes once in a while
                i += 1
                if i % 15 == 0:
                    print("Writing to db...")
                    conn.commit()
            else:
                print("Cannot get apartment info for apartment " + apartment["object_id"])
            # sleep so we don't dos the site
            time.sleep(random.uniform(1.5, 3.5))
        conn.commit()
        print("Finished, going to sleep now...")
        conn.close()
    else:
        print("GET failed")

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(e)
        # repeat in an hour if finished
        time.sleep(3600)


