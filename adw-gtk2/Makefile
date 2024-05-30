TARGET		:= adw-gtk3
INSTALL_DIR	:= $(PREFIX)/usr/share/themes
INSTALL		:= rsync -a -delete

.SUFFIXES:

.PHONY: install uninstall FORCE

all:

clean:

FORCE:

$(INSTALL_DIR)/$(TARGET):
	mkdir -p $@

$(INSTALL_DIR)/$(TARGET)-dark:
	mkdir -p $@

$(INSTALL_DIR)/$(TARGET)/gtk-2.0: adw-gtk3/gtk-2.0/ FORCE | $(INSTALL_DIR)/$(TARGET)
	$(INSTALL) $< $@

$(INSTALL_DIR)/$(TARGET)-dark/gtk-2.0: adw-gtk3-dark/gtk-2.0/ FORCE | $(INSTALL_DIR)/$(TARGET)-dark
	$(INSTALL) $< $@

install: $(INSTALL_DIR)/$(TARGET)/gtk-2.0 $(INSTALL_DIR)/$(TARGET)-dark/gtk-2.0

uninstall:
	rm -rf $(INSTALL_DIR)/$(TARGET)/gtk-2.0
	rm -rf $(INSTALL_DIR)/$(TARGET)-dark/gtk-2.0
