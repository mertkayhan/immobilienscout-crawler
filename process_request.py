import requests
import logging
import pickle
import os.path
import dateutil.parser


logging.basicConfig(filename='search-apartment.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=0)


class RequestApartments(object):
    def __init__(self):

        """ Initialize internal memory
        :type self:
        :param self:

        :raises:

        :rtype:
        """

        self.__idx = set()

    def __save_records(self):

        """ Save internal memory in binary format
        :type self:
        :param self:

        :raises:

        :rtype:
        """

        with open("records.pickle", "wb") as p:
            pickle.dump(self.__idx, p)

    def __load_records(self):

        """ Load previous internal state
        :type self:
        :param self:

        :raises:

        :rtype:
        """

        with open("records.pickle", "rb") as p:
            r = pickle.load(p)
        return r

    def __receive_apartment_data(self, link):

        """ Query for apartments
        :type self:
        :param self:

        :type link: str
        :param link: query link

        :raises:

        :rtype: None if the query is empty, data container otherwise
        """

        data = requests.post(link).json()["searchResponseModel"]["resultlist.resultlist"]["resultlistEntries"][0]
        if int(data["@numberOfHits"]) == 0:
            logging.warning("Found no apartmens!")
            return None
        logging.info("Query returned {} apartments".format(
            data["@numberOfHits"])
        )
        return data["resultlistEntry"]

    def __process_apartment_data(self, data):

        """ Parse queried data and get rid of unuseful information
        :type self:
        :param self:

        :type data: dict
        :param data: data returned by the query

        :raises:

        :rtype: return a list of new apartments
        """

        new_apartments = []

        for entry in data:
            apartment_id = int(entry["@id"])

            if apartment_id in self.__idx:
                continue

            self.__idx.add(apartment_id)

            try:
                title = "{}".format(entry["resultlist.realEstate"]["title"])
            except KeyError:
                title = ""
            try:
                addr = "{} {} {} {} {}".format(
                    entry["resultlist.realEstate"]["address"]["street"],
                    entry["resultlist.realEstate"]["address"]["houseNumber"],
                    entry["resultlist.realEstate"]["address"]["postcode"],
                    entry["resultlist.realEstate"]["address"]["city"],
                    entry["resultlist.realEstate"]["address"]["quarter"]
                )
            except KeyError:
                addr = ""
            try:
                price = "{} {}".format(
                    entry["resultlist.realEstate"]["price"]["value"],
                    entry["resultlist.realEstate"]["price"]["currency"]
                )
            except KeyError:
                price = ""
            try:
                space = "{}".format(
                    entry["resultlist.realEstate"]["livingSpace"]
                )
            except KeyError:
                space = ""
            try:
                num_rooms = "{}".format(
                    entry["resultlist.realEstate"]["numberOfRooms"]
                )
            except KeyError:
                num_rooms = ""
            try:
                kitchen = "{}".format(
                    entry["resultlist.realEstate"]["builtInKitchen"]
                )
            except KeyError:
                kitchen = ""
            try:
                balcony = "{}".format(
                    entry["resultlist.realEstate"]["balcony"]
                )
            except KeyError:
                balcony = ""
            try:
                publish_date = "{}".format(
                    dateutil.parser.parse(entry["@publishDate"])
                )
            except KeyError:
                publish_date = ""
            try:
                calc_price = "{} {}".format(
                    entry["resultlist.realEstate"]["calculatedPrice"]["value"],
                    entry["resultlist.realEstate"]["calculatedPrice"]["currency"]
                )
            except KeyError:
                calc_price = ""

            apartment_info = {
                "title": title,
                "address": addr,
                "price": price,
                "livingSpace": space,
                "numberOfRooms": num_rooms,
                "builtInKitchen": kitchen,
                "balcony": balcony,
                "publishDate": publish_date,
                "calculatedPrice": calc_price
            }
            new_apartments.append(apartment_info)

        return new_apartments

    def run(self, link):

        """ Main function
        :type self:
        :param self:

        :type link: str
        :param link: query link

        :raises:

        :rtype: None if query is empty, new apartments otherwise
        """

        if os.path.exists("records.pickle") and os.path.getsize("records.pickle") > 0:
            self.__idx = self.__load_records()
        data = self.__receive_apartment_data(link)
        if data:
            new_apartments = self.__process_apartment_data(data)
            self.__save_records()
            return new_apartments
        return None


if __name__ == "__main__":
    pass
