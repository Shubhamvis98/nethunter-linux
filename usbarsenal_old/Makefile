CC = $(CROSS_COMPILE)gcc
INSTALLDIR = /usr/local/bin

all: hidg

hidg: hid-gadget-test.c
	$(CC) $< -o $@

install: all
	install -m 0755 usbarsenal $(INSTALLDIR)/usbarsenal
	install -m 0755 hidg $(INSTALLDIR)/hidg
	install -m 0755 duckyconverter $(INSTALLDIR)/duckyconverter
	install -m 0755 duckyprint $(INSTALLDIR)/duckyprint

uninstall:
	@rm $(INSTALLDIR)/hidg
	@rm $(INSTALLDIR)/duckyconverter
	@rm $(INSTALLDIR)/duckyprint
	@rm $(INSTALLDIR)/usbarsenal

clean:
	@rm hidg

