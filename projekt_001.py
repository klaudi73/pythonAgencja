# -*- coding: utf-8 -*-
#
#               plik projekt_001.py
#
#--------------------------------------------------#
#                                                  #
#   Projekt oprogramowania bazy danych 'agencja'   #
#                                                  #
#--------------------------------------------------#

import pymysql;
#import sys;
import os;

class Agencja:
    def __init__(self):
        self.menu();
    
    def menu(self):
        var = os.system('cls');
        print("Program obsługi bazy danych 'agencja'");
        while(True):
            print("1. Zaloguj, 0. Wyjdż ");
            decyzja = int(input(": "));
            if decyzja == 1:
                self.connstring();
                perm = self.login();
                print("Połączenie ustanowione.");
                if perm[0][0].upper() == 'A':
                    self.obsluga_administracyjna();
                elif perm[0][0].upper() == 'U':
                    self.obsluga_uzytkownika();
            elif decyzja == 0:
                break;
            else:
                print("Zły wybór!");
                print("Spróbuj jeszcze raz...");
        os.sys.exit(0);
        
    def connstring(self):
        self.conn = pymysql.connect("localhost", "agent", "agent", "agencja", charset="utf8", use_unicode=True);
        self.c = self.conn.cursor();
    
    def login(self):
        self.connstring();
        login = input("login: ");
        password = input("hasło: ");
        self.c.execute("SELECT users__perm FROM users WHERE users__login=%s and users__pass=%s;", (login, password));
        try:
            perm = self.c.fetchall();
        except:
            perm = 0;
        if perm == "":
            perm = 0;
        return perm;
    
    def obsluga_administracyjna(self):
        pass;
    
    def obsluga_uzytkownika(self):
        while(True):
            print("1. Wprowadzanie danych klientów");
            print("2. Dzwonienie do klientów");
            print("3. Lista spotkań");
            print("4. Efekty spotkania");
            print("5. Wprowadzanie wniosku ubezpieczeniowego");
            print("6. Wprowadzanie umowy");
            print("7. Lista wniosków i umów");
            print("0. Wylogowanie i zakończenie programu");
            decyzja = int(input(": "));
            if decyzja == 1:
                self.wprowadzDaneKlientow("u");
            elif decyzja == 2:
                self.dzwonDoKlientow("u");
            elif decyzja == 3:
                self.listaSpotkanZKlientami("u");
            elif decyzja == 4:
                self.efektySpotkania("u");
            elif decyzja == 5:
                self.wprowadzWniosekUbezpieczeniowy("u");
            elif decyzja == 6:
                self.wprowadzUmowe("u");
            elif decyzja == 7:
                self.listaWnioskowUmow("u");
            elif decyzja == 0:
                self.c.close();
                break;
            else:
                continue;
        os.sys.exit(0);
            
    def wyswietl_lista_dzwonienia_po_1_rekord(self):
        result = self.c.execute("SELECT * FROM lista_dzwonienia WHERE dzw__zadzwonione = 0 ORDER BY dzw__kiedyzadzwonic;");
        for row in self.c.fetchall():
            dzwonienie__ID = row[0];
            dzw__kiedyzadzwonic = row[1];
            dzw__zadzwonione = row[2];
            klient_klient__ID = row[3];
            klient__ID = row[4];
            klient__imie = row[5];
            klient__nazwisko = row[6];
            klient__pesel = row[7]
            klient__numertelefonu = row[8];
            
            print("           Imię: %20s" % klient__imie);
            print("");
            print("       Nazwisko: %20s" % klient__nazwisko);
            print("");
            print(" Numer telefonu: %20s" % klient__numertelefonu);
            print("");
            print("          PESEL: %20s" % klient__pesel);
            print("");
            print("Kiedy zadzwonić: %20s" % dzw__kiedyzadzwonic);
            print("");

            print("Czy udało się zadzwonić?");
            print("1 - Tak, 2 - Nie");
            decyzja = int(input(": "));
            if decyzja == 1:
                self.update_dzwonienie(dzwonienie__ID);
                print("Trzeba umówić spotkanie");
                self.umow_spotkanie(klient__ID);
                
            elif decyzja == 2:
                pass;
            
            print("Zadzwonić do kolejnego klienta?");
            print("1 - Tak, 0 - Nie");
            decyzja2 = int(input(": "));
            if decyzja2 == 1:
                continue;
            else:
                break;
    
    def umow_spotkanie(self, klient__ID):
        while(True):
            self.wyswietl_miejsca_spotkan();
            print("Czy miejsce spotkań jest na liście powyżej?");
            print("Jeśli tak, podaj wartość kolumny 'miejsca__ID', w przeciwnym wypadku podaj '0'");
            decyzja3 = int(input(": "));
            if decyzja3 == 0:
                self.dodaj_miejsce_spotkan();
                continue;
            else:
                self.ustaw_spotkanie(klient__ID, decyzja3);
                break;
        
    def dodaj_miejsce_spotkan(self):
        spotkania_miejsca__nazwa_miejsca = input("Podaj nazwę miejsca: ");
        spotkania_miejsca__ulica = input("Podaj ulicę: ");
        spotkania_miejsca__nr_domu = input("Podaj numer domu: ");
        spotkania_miejsca__nr_lokalu = input("Podaj numer lokalu: ");
        spotkania_miejsca__miasto = input("Podaj miasto: ");
        spotkania_miejsca__panstwo = input("Podaj państwo: ");
        spotkania_miejsca__opis = input("Podaj opis: ");
        self.conn2 = pymysql.connect("localhost", "agent", "agent", "agencja", charset="utf8", use_unicode=True);
        self.c2 = self.conn2.cursor();
        zapytanie_do_bazy = "INSERT INTO " + \
                            "spotkania_miejsca " + \
                            "(spotkania_miejsca__nazwa_miejsca, spotkania_miejsca__ulica, " + \
                            "spotkania_miejsca__nr_domu, spotkania_miejsca__nr_lokalu, spotkania_miejsca__miasto, " + \
                            "spotkania_miejsca__panstwo, spotkania_miejsca__opis) " + \
                            "VALUES (\"" + \
                            spotkania_miejsca__nazwa_miejsca + "\", \"" + \
                            spotkania_miejsca__ulica + "\", \"" + \
                            spotkania_miejsca__nr_domu + "\", \"" + \
                            spotkania_miejsca__nr_lokalu + "\", \"" + \
                            spotkania_miejsca__miasto + "\", \"" + \
                            spotkania_miejsca__panstwo + "\", \"" + \
                            spotkania_miejsca__opis + \
                            "\");"
        print(zapytanie_do_bazy);
        result = self.c2.execute(zapytanie_do_bazy);
        self.conn2.commit();
        self.conn2.close();
    
    def ustaw_spotkanie(self, klient__ID, miejsce__ID):
        spot__termin = input("Podaj termin spotkania (YYYY-MM-DD, HH:MM): ");
        while(True):
            przypomniec = input("Czy przypomnieć o spotkaniu? (1 - Tak, 0 - Nie): ");
            if przypomniec == "1":
                spot__przypomnienie_dni = input("Podaj ile dni przed spotkaniem przypomnieć: ");
                if spot__przypomnienie_dni == "":
                    spot__przypomnienie_dni = "0";
                spot__przypomnienie_godz = input("Podaj ile godzin przed spotkaniem przypomnieć: ");
                if spot__przypomnienie_godz == "":
                    spot__przypomnienie_godz = "0";
                spot__przypomnienie_min = input("Podaj ile minut przed spotkaniem przypomnieć: ");
                if spot__przypomnienie_min == "":
                    spot__przypomnienie_min = "0";
                break;
            elif przypomniec == "0":
                spot__przypomnienie_dni = "0";
                spot__przypomnienie_godz = "0";
                spot__przypomnienie_min = "0";
                break;
            else:
                continue;
        
        self.conn3 = pymysql.connect("localhost", "agent", "agent", "agencja", charset="utf8", use_unicode=True);
        self.c3 = self.conn3.cursor();
        zapytanie_do_bazy1 = "INSERT INTO " + \
                            "spotkanie " + \
                            "(spot__termin, " + \
                            "spot__przypomnienie_dni, spot__przypomnienie_godz, spot__przypomnienie_min, " + \
                            "spot__odbylo_sie, klient_klient__ID) " + \
                            "VALUES (\"" + \
                            spot__termin + "\", \"" + \
                            spot__przypomnienie_dni + "\", \"" + \
                            spot__przypomnienie_godz + "\", \"" + \
                            spot__przypomnienie_min + "\", 0, \"" + \
                            str(klient__ID) + \
                            "\");";
        zapytanie_do_bazy2 = "INSERT INTO " + \
                            "spotkanie_miejsce " + \
                            "(spotkania_miejsca_spotkanie_miejsce__ID, spotkanie_spotkanie__ID) " + \
                            "VALUES (\"" + str(miejsce__ID) + "\", last_insert_id());";
        self.conn3.autocommit(False);
        self.conn3.begin();
        self.c3.execute(zapytanie_do_bazy1);
        self.c3.execute(zapytanie_do_bazy2);
        self.conn3.commit();
        self.conn3.close();
    
    def wyswietl_miejsca_spotkan(self):
        self.conn3 = pymysql.connect("localhost", "agent", "agent", "agencja", charset="utf8", use_unicode=True);
        self.c3 = self.conn3.cursor();
        result = self.c3.execute("SELECT * FROM spotkania_miejsca;");
        print("");
        print("                                             spotkania                                                   ");
        print("miejsca|       nazwa        |                  | nr |nr    |             |                 |");
        print(" __ID  |      miejsca       |       ulica      |domu|lokalu|   miasto    |     państwo     |    opis");
        print("-------+--------------------+------------------+----+------+-------------+-----------------+-------------");
        for row in self.c3.fetchall():
            spotkania_miejsca__ID = row[0];
            spotkania_miejsca__nazwa_miejsca = row[1];
            spotkania_miejsca__ulica = row[2];
            spotkania_miejsca__nr_domu = row[3];
            spotkania_miejsca__nr_lokalu = row[4];
            spotkania_miejsca__miasto = row[5];
            spotkania_miejsca__panstwo = row[6];
            spotkania_miejsca__opis = row[7];
            
            print("%7i" % spotkania_miejsca__ID, end="|");
            print("%20.20s" % spotkania_miejsca__nazwa_miejsca, end="|");
            print("%18.18s" % spotkania_miejsca__ulica, end="|");
            print("%4.4s" % spotkania_miejsca__nr_domu, end="|");
            print("%6.6s" % spotkania_miejsca__nr_lokalu, end="|");
            print("%13.13s" % spotkania_miejsca__miasto, end="|");
            print("%17.17s" % spotkania_miejsca__panstwo, end="|");
            print("%-22.22s" % spotkania_miejsca__opis);
        print("");
        self.c3.close();
        
    
    def update_dzwonienie(self, dzwonienie__ID):
        self.conn2 = pymysql.connect("localhost", "agent", "agent", "agencja", charset="utf8", use_unicode=True);
        self.c2 = self.conn2.cursor();
        result = self.c2.execute("UPDATE dzwonienie SET dzw__zadzwonione = 1 WHERE dzwonienie__ID = " + str(dzwonienie__ID) + ";");
        self.conn2.commit();
        self.conn2.close();
    
    def wyswietl_lista_dzwonienia(self):
        result = self.c.execute("SELECT * FROM lista_dzwonienia WHERE dzw__zadzwonione = 0;");
        print("");
        print("dzwonienie|       Kiedy        |    Czy     | klient |                  |                   |      Numer      |");
        print("   __ID   |     zadzwonić?     |zadzwonione?|  __ID  |       Imię       |      Nazwisko     |     telefonu    |    PESEL");
        print("----------+--------------------+------------+--------+------------------+-------------------+-----------------+-------------");
        for row in self.c.fetchall():
            dzwonienie__ID = row[0];
            dzw__kiedyzadzwonic = row[1];
            dzw__zadzwonione = row[2];
            klient_klient__ID = row[3];
            klient__ID = row[4];
            klient__imie = row[5];
            klient__nazwisko = row[6];
            klient__pesel = row[7]
            klient__numertelefonu = row[8];
            
            print("%10i" % dzwonienie__ID, end="|");
            print("%20s" % dzw__kiedyzadzwonic, end="|");
            print("%12s" % dzw__zadzwonione, end="|");
            print("%8i" % klient__ID, end="|");
            print("%18s| %18s" % (klient__imie, klient__nazwisko), end="|");
            print("%17s" % klient__numertelefonu, end="|");
            print("%12s" % klient__pesel);
        print("");
        
    def wprowadzDaneKlientow(self, typ_uzytkownika):
        print("Podaj nazwę pliku.");
        sciezka = input("Plik: ");
        plik = open(sciezka, "r");
        rekord = [];
        try:
            connWprowadzDaneK = pymysql.connect("localhost", "agent", "agent", "agencja", charset="utf8", use_unicode=True);
            cursorWprowadzDaneK = connWprowadzDaneK.cursor();
            connWprowadzDaneK.begin();
            for linia in plik:
                print(linia);
                linia2 = linia.replace("\"", "");
                print(linia2);
                linia3 = linia2.replace("\n", "");
                print(linia3);
                rekord = linia3.split(";");
                print(rekord);
                if rekord[0] == "klient__imie":
                    continue;
                else:
                    zapytanie1 = "INSERT INTO klient (klient__imie, klient__nazwisko, klient__pesel, klient__numertelefonu) " + \
                        "VALUES (\"" + rekord[0] + "\", \"" + rekord[1] + "\", \"" + rekord[2] + "\", \"" + rekord[3]+ "\");";
                    print(zapytanie1);
                    cursorWprowadzDaneK.execute(zapytanie1);
            connWprowadzDaneK.commit();
        except pymysql.MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]));
            connWprowadzDaneK.rollback();
        except pymysql.InternalError as error:
            code, message = error.args;
            print(">>>>>>>>>>>>>", code, message);
        except:
            print("Ups! Cos poszło nie tak.");
        finally:
            connWprowadzDaneK.close();
            plik.close();

        
    def dzwonDoKlientow(self, typ_uzytkownika):
        var = os.system('cls');
        print("Lista klientów do których należy zadzwonić.");
        self.wyswietl_lista_dzwonienia();
        while(True):
            print("1. Zadzwoń");
            print("0. Powrót");
            decyzja = int(input(": "));
            if decyzja == 1:
                self.wyswietl_lista_dzwonienia_po_1_rekord();
                break;
            elif decyzja == 2:
                break;
            elif decyzja == 3:
                break;
            elif decyzja == 0:
                break;
            else:
                continue;

    def efektySpotkania(self, typ_uzytkownika):
        self.listaSpotkanZKlientami(typ_uzytkownika, "lista");
        print("Które spotkanie odbyłeś?");
        print("Podaj \"Spot__ID\" lub \"0\" jeśli nie odbyłeś żadnego spotkania");
        spotkanie__ID = input("Spot.__ID: ");
        if spotkanie__ID == "0":
            pass;
        else:
            efekt__opis = input("Opis: ");
            try:
                self.connDodajEfektSpotkania = pymysql.connect("localhost", "agent", "agent", "agencja", charset="utf8", use_unicode=True);
                self.cursorDodajEfektSpotkania = self.connDodajEfektSpotkania.cursor();
                self.connDodajEfektSpotkania.begin();
                zapytanie1 = "INSERT INTO efekt_spotkania (efekt__opis, spotkanie_spotkanie__ID) VALUES (\"" + efekt__opis + "\", \"" + spotkanie__ID + "\");";
                zapytanie2 = "UPDATE spotkanie SET spot__odbylo_sie = 1 WHERE spotkanie__ID = " + str(spotkanie__ID) + ";";
                print("Zapytanie: " + zapytanie2);
                self.cursorDodajEfektSpotkania.execute(zapytanie1);
                self.cursorDodajEfektSpotkania.execute(zapytanie2);
                self.connDodajEfektSpotkania.commit();
                print("Informacje zapisane.");
            except:
                self.connDodajEfektSpotkania.rollback();
                print("Ups. Coś poszło nie tak.");
            finally:
                self.connDodajEfektSpotkania.close();

    def listaSpotkanZKlientami(self, typ_uzytkownika, typ_zapytania = "lista"):
        self.connListaSpotkan = pymysql.connect("localhost", "agent", "agent", "agencja", charset="utf8", use_unicode=True);
        self.cursorListaSpotkan = self.connListaSpotkan.cursor();
        self.connListaSpotkan.begin();
        if typ_zapytania == "lista":
            zapytanie = "SELECT * FROM lista_spotkan_z_klientami;";
        elif typ_zapytania == "wnioski":
            zapytanie = "SELECT * FROM mozliwe_wnioski;";
        else:
            pass;
        result = self.cursorListaSpotkan.execute(zapytanie);
        self.connListaSpotkan.commit();
        print("");
        print("spot.|   termin           | klient |                  |                   |      Numer      |            |  Nazwa   |            |    |      |        |         ");
        print("__ID |   spotkania        |  __ID  |       Imię       |      Nazwisko     |     telefonu    |    PESEL   | Miejsca  |   Ulica    | Nr | Lok. | Miasto | Państwo ");
        print("-----+--------------------+--------+------------------+-------------------+-----------------+------------+----------+------------+----+------+--------+---------");
        for row in self.cursorListaSpotkan.fetchall():
            spotkanie__ID = row[0];
            spot__termin = row[1];
            klient__ID = row[7];
            klient__imie = row[8];
            klient__nazwisko = row[9];
            klient__pesel = row[10];
            klient__numertelefonu = row[11];
            spotkania_miejsca__ID = row[12];
            spotkania_miejsca__nazwa_miejsca = row[13];
            spotkania_miejsca__ulica = row[14];
            spotkania_miejsca__nr_domu = row[15];
            spotkania_miejsca__nr_lokalu = row[16];
            spotkania_miejsca__miasto = row[17];
            spotkania_miejsca__panstwo = row[18];
            print("%5i" % spotkanie__ID, end="|");
            print("%20.20s" % spot__termin, end="|");
            print("%8i" % klient__ID, end="|");
            print("%18.18s| %18.18s" % (klient__imie, klient__nazwisko), end="|");
            print("%17.17s" % klient__numertelefonu, end="|");
            print("%12.12s" % klient__pesel, end ="|");
            print("%10.10s" % spotkania_miejsca__nazwa_miejsca, end ="|");
            print("%12.12s" % spotkania_miejsca__ulica, end="|");
            print("%4.4s" % spotkania_miejsca__nr_domu, end="|");
            print("%6.6s" % spotkania_miejsca__nr_lokalu, end="|");
            print("%8.8s" % spotkania_miejsca__miasto, end="|");
            print("%8.8s" % spotkania_miejsca__panstwo);
        print("");
        self.connListaSpotkan.close();

    def wprowadzWniosekUbezpieczeniowy(self, typ_uzytkownika):
        self.listaSpotkanZKlientami(typ_uzytkownika, "wnioski");
        print("Dla którego spotkania wypełniamy wniosek?");
        print("Podaj \"Spot.__ID\", jeżeli nie wypełniamy wniosku, wpisz \"0\".");
        spotkanie__ID = input("Spot.__ID: ");
        if spotkanie__ID == "0":
            pass;
        else:
            wniosek__numer_wniosku = input("Podaj numer wniosku: ");
            wniosek__stawka_uroczniona = input("Podaj stawkę urocznioną: ");
            print("Podaj częstotliwość opłacania składek w miesiącach");
            wniosek__czestotliwosc = input("(1 - co miesiąc, 3 - co kwartał, 6 - co pół roku, 12 - co rok): ");
            wniosek__czas_trwania = input("Podaj czas trwania ubezpieczenia w miesiącach: ");
            self.wyswietlListeProduktow("produkty");
            produkt__ID = input("Podaj Produkt__ID: ");
            lista_produktow=[];
            lista_produktow.append(produkt__ID);
            print("Czy są jakieś umowy dodatkowe?")
            decyzja = input("1 - Tak, 0 - Nie: ");
            if decyzja == "1":
                self.wyswietlListeProduktow("podprodukty", produkt__ID);
                produkty_produkty__ID___lista = input("Podaj listę podproduktów (Produkt__ID) oddzielając je przecinkami: ");
                lista_produktow.extend(produkty_produkty__ID___lista.split(","));
                
            else:
                pass;
            
            try:
                connWprowadzWniosek = pymysql.connect("localhost", "agent", "agent", "agencja", charset="utf8", use_unicode=True);
                cursorWprowadzWniosek = connWprowadzWniosek.cursor();
                connWprowadzWniosek.begin();
                zapytanie0 = "SELECT klient__ID FROM mozliwe_wnioski WHERE spotkanie__ID = " + spotkanie__ID + ";";
                cursorWprowadzWniosek.execute(zapytanie0);
                klient_klient__ID = cursorWprowadzWniosek.fetchone();
                zapytanie1 = "INSERT INTO wniosek " + \
                    "(wniosek__numer_wniosku, wniosek__stawka_uroczniona, wniosek__czestotliwosc, wniosek__czas_trwania, " + \
                    "klient_klient__ID) " + \
                    "VALUES (" + wniosek__numer_wniosku + ", " + wniosek__stawka_uroczniona + ", " + \
                    wniosek__czestotliwosc + ", " + wniosek__czas_trwania + ", " + \
                    str(klient_klient__ID[0]) + ");";
                cursorWprowadzWniosek.execute(zapytanie1);
                wniosek__ID = cursorWprowadzWniosek.lastrowid;
                for produkty_produkty__ID in lista_produktow:
                    zapytanie2 = "INSERT INTO wniosek_produkty " + \
                        "(wniosek_wniosek__ID, wniosek_produkt__ID) " + \
                        "VALUES (" + str(wniosek__ID) + ", " + produkty_produkty__ID + ");";
                    cursorWprowadzWniosek.execute(zapytanie2);
                zapytanie3 = "UPDATE spotkanie SET spot__odbylo_sie = 2 WHERE spotkanie__ID = " + str(spotkanie__ID) + ";";
                cursorWprowadzWniosek.execute(zapytanie3);
                connWprowadzWniosek.commit();
                print("Informacje zapisane.");
            except:
                connWprowadzWniosek.rollback();
                print("Ups. Coś poszło nie tak.");
            finally:
                connWprowadzWniosek.close();

    def wyswietlListeProduktow(self, typ_produktow, produkt__ID = 0, wyswietl_naglowek = 1, produkty_zaleznosc__parent__ID = 0):
        try:
            connWyswietlProdukty = pymysql.connect("localhost", "agent", "agent", "agencja", charset="utf8", use_unicode=True);
            cursorWyswietlProdukty = connWyswietlProdukty.cursor();
            connWyswietlProdukty.begin();
            if typ_produktow == "produkty":
                zapytanie1 = "SELECT * FROM podprodukty WHERE produkty_zaleznosc__parent__ID = 0;";
            elif typ_produktow == "podprodukty":
                zapytanie1 = "SELECT * FROM podprodukty WHERE produkty_zaleznosc__parent__ID = " + produkt__ID + ";";
            elif typ_produktow == "produkt":
                zapytanie1 = "SELECT * FROM podprodukty WHERE produkty__ID = " + str(produkt__ID) + ";";
            elif typ_produktow == "produkt2":
                zapytanie1 = "SELECT * FROM podprodukty WHERE produkty__ID = " + str(produkt__ID) + " AND produkty_zaleznosc__parent__ID = " + str(produkty_zaleznosc__parent__ID) + ";";
            else:
                pass;
            cursorWyswietlProdukty.execute(zapytanie1);
            connWyswietlProdukty.commit();
            if wyswietl_naglowek == 1:
                print("");
                print("produkty|                     produkt                    |                           produkt                    ");
                print("  __ID  |                     nazwa                      |                             opis                     ");
                print("--------+------------------------------------------------+------------------------------------------------------");

            for row in cursorWyswietlProdukty.fetchall():
                produkty__ID = row[0];
                prod__nazwa = row[1];
                prod__opis = row[2];
                
                print("%8i" % produkty__ID, end="|");
                print("%48.48s" % prod__nazwa, end="|");
                print("%60.60s" % prod__opis);
        except:
            connWyswietlProdukty.rollback();
            print("Ups. Coś poszło nie tak.");
        finally:
            connWyswietlProdukty.close();
        
    def wyswietlWnioski(self):
        connWyswietlWnioski = pymysql.connect("localhost", "agent", "agent", "agencja", charset="utf8", use_unicode=True);
        cursorWyswietlWnioski = connWyswietlWnioski.cursor();
        connWyswietlWnioski.begin();
        zapytanie1 = "SELECT * FROM lista_wnioskow_bez_umow;";
        
        cursorWyswietlWnioski.execute(zapytanie1);
        listaWnioskow = [];
        for row in cursorWyswietlWnioski.fetchall():
            listaWnioskow.append(row);
        zapytanie2 = "SELECT DISTINCT wniosek_wniosek__ID FROM wniosek_produkty;";
        cursorWyswietlWnioski.execute(zapytanie2);
        wnioski = [];
        for row in cursorWyswietlWnioski.fetchall():
            wnioski.append(row[0]);
        
        print("Lista wnioskow:");
        print("       |           |          |częstotliwość|       |      ");
        print("       |           |          |   [ilość    |       |      ");
        print("wniosek|   numer   |  stawka  |    wpłat    |  czas |klient");
        print("  __ID |  wniosku  |uroczniona|   rocznie]  |trwania| __ID" );
        print("-------+-----------+----------+-------------+-------+------");
        formatowanie = [7,11,10,13,7,6];
        for wniosek in wnioski:
            for j in range(0,len(listaWnioskow)):
                if listaWnioskow[j][0] == wniosek:
                    for i in range(0,len(listaWnioskow[j])):
                        napis = "%" + str(formatowanie[i]) + "." + str(formatowanie[i]) + "s";
                        print(napis % str(listaWnioskow[j][i]), end=("|"));
                    print("");
        connWyswietlWnioski.close();
        
    def wprowadzUmowe(self, typ_uzytkownika):
        self.wyswietlWnioski();
        decyzja = input("Podaj numer wniosku [wniosek__ID] do umowy: ");
        result = self.wyswietlWniosek(decyzja);
        if result == 0:
            pass;
        else:
            print("Podaj datę rozpoczęcia umowy.");
            data = input("YYYY-MM-RR: ");
            try:
                connWprowadzUmowe = pymysql.connect("localhost", "agent", "agent", "agencja", charset="utf8", use_unicode=True);
                cursorWprowadzUmowe = connWprowadzUmowe.cursor();
                connWprowadzUmowe.begin();
                zapytanie1 = "INSERT INTO umowa (umowa__data_rozpoczecia, wniosek_wniosek__ID) " + \
                    "VALUES (\"" + data + "\", " + str(decyzja) + ");";
                print(zapytanie1);
                cursorWprowadzUmowe.execute(zapytanie1);
                connWprowadzUmowe.commit();
            except:
                connWprowadzUmowe.rollback();
                print("Ups! Coś poszło nie tak.");
            finally:
                connWprowadzUmowe.close();
        
    def wyswietlWniosek(self, wniosek__ID):
        connWyswietlWniosek = pymysql.connect("localhost", "agent", "agent", "agencja", charset="utf8", use_unicode=True);
        cursorWyswietlWniosek = connWyswietlWniosek.cursor();
        connWyswietlWniosek.begin();
        zapytanie1 = "SELECT * FROM wniosek WHERE wniosek__ID = " + wniosek__ID + ";";
        cursorWyswietlWniosek.execute(zapytanie1);
        print("\nWniosek: " + wniosek__ID);
        print("           |          |częstotliwość|       |      ");
        print("           |          |   [ilość    |       |      ");
        print("   numer   |  stawka  |    wpłat    |  czas |klient");
        print("  wniosku  |uroczniona|   rocznie]  |trwania| __ID" );
        print("-----------+----------+-------------+-------+------");
        formatowanie = [7,11,10,13,7,6];
        for row in cursorWyswietlWniosek.fetchall():
            for i in range(1,len(row)):
                napis = "%"+str(formatowanie[i])+"."+str(formatowanie[i])+"s";
                print(napis % str(row[i]), end=("|"));
                if i == 5:
                    klient__ID = row[i];
            print("");
        print("\nKlient o ID " + str(klient__ID) + ": ");
        self.wyswietlKlienta(klient__ID);
        zapytanie2 ="SELECT wniosek_produkt__ID FROM wniosek_produkty AS w JOIN produkty_zaleznosc AS p ON w.wniosek_produkt__ID = p.produkty_produkty__ID " + \
            "WHERE w.wniosek_wniosek__ID = " + str(wniosek__ID) + " and p.produkty_zaleznosc__parent__ID = 0;";
        cursorWyswietlWniosek.execute(zapytanie2);
        row = cursorWyswietlWniosek.fetchone();
        produkt__ID = row[0];
        print("");
        self.wyswietlListeProduktow("produkt", produkt__ID, 1)
        zapytanie3 = "SELECT wniosek_produkt__ID FROM wniosek_produkty WHERE wniosek_wniosek__ID = " + str(wniosek__ID) + " AND wniosek_produkt__ID != " + str(produkt__ID) + ";";
        print("");
        cursorWyswietlWniosek.execute(zapytanie3);
        for row in cursorWyswietlWniosek.fetchall():
            tempProdukt__ID = int(row[0]);
            self.wyswietlListeProduktow("produkt2", tempProdukt__ID, 0, produkt__ID);
        print("\nCzy to jest właściwy wniosek?");
        decyzja = input("1 - Tak, 0 - Nie: ");
        connWyswietlWniosek.close();
        if decyzja == "1":
            return wniosek__ID;
        else:
            return 0;
        
    def wyswietlKlienta(self, klient__ID):
        connWyswietlKlienta = pymysql.connect("localhost", "agent", "agent", "agencja", charset="utf8", use_unicode=True);
        cursorWyswietlKlienta = connWyswietlKlienta.cursor();
        connWyswietlKlienta.begin();
        zapytanie1 = "SELECT * FROM klient WHERE klient__ID = " + str(klient__ID) + ";";
        cursorWyswietlKlienta.execute(zapytanie1);
        print("klient|           |              |           |       numer     ");
        print(" __ID |   imię    |   nazwisko   |   PESEL   |     telefonu    ");
        print("------+-----------+--------------+-----------+-----------------");
        formatowanie = [6,11,14,11,17];
        row = cursorWyswietlKlienta.fetchone();
        for i in range(0,len(row)):
            napis = "%" + str(formatowanie[i]) + "." + str(formatowanie[i]) + "s";
            print(napis % str(row[i]), end=("|"));
        print("");
        
    
    def listaWnioskowUmow(self, typ_uzytkownika):
        connWyswietlWnUm = pymysql.connect("localhost", "agent", "agent", "agencja", charset="utf8", use_unicode=True);
        cursorWyswietlWnUm = connWyswietlWnUm.cursor();
        connWyswietlWnUm.begin();
        zapytanie1 = "SELECT * FROM wniosek;";
        zapytanie2 = "SELECT * FROM umowa;";
        cursorWyswietlWnUm.execute(zapytanie1);
        print("\nLista wniosków: ");
        for row in cursorWyswietlWnUm.fetchall():
            print(row);
        cursorWyswietlWnUm.execute(zapytanie2);
        print("\nLista umów: ");
        for row in cursorWyswietlWnUm.fetchall():
            print(row);
        connWyswietlWnUm.commit();
        connWyswietlWnUm.close();
        
            
a=Agencja();