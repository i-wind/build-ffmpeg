CURRENT_TIME = $(shell date +"%F %H:%M:%S")
TARGETS := lame faac x264 sdl ffmpeg
CDIR := $(CURDIR)
USR  := $(CDIR)/usr
UID  := $(shell id -u)
LOG_FILE := $(CDIR)/build_$(shell date +"%Y%m%d_%H%M%S").log

LAME_DIR   := lame-3.99.5
FAAC_DIR   := faac-1.28
SDL_DIR    := SDL-1.2.15
FFMPEG_DIR := ffmpeg-2.6.3
DIRS := $(LAME_DIR) $(FAAC_DIR) x264 $(FFMPEG_DIR)

export C_USR_DIR = $(USR)
export C_INCLUDE_PATH = $(USR)/include/
export LIBRARY_PATH = $(USR)/lib/

ifeq ($(UID),0)
	SUDO :=
else
	SUDO := sudo
endif

.PHONY: all build $(TARGETS)

all: build $(TARGETS)
	echo "$(CURRENT_TIME) done building..." >> ${LOG_FILE}

build:
	mkdir -p ${C_USR_DIR}
	echo "$(CURRENT_TIME) start building..." >> ${LOG_FILE}

lame:
	cd $(LAME_DIR); \
	echo -n "$(CURRENT_TIME) building $@ ... " >> $(LOG_FILE); \
	./configure --prefix=$(C_USR_DIR) --enable-shared --enable-static >> ${LOG_FILE} 2>&1; \
	$(MAKE) >> ${LOG_FILE} 2>&1 && $(MAKE) install;

faac:
	cd $(FAAC_DIR); \
	echo -n "$(CURRENT_TIME) building $@ ... " >> $(LOG_FILE); \
	./configure --prefix=$(C_USR_DIR) --enable-shared --enable-static >> ${LOG_FILE} 2>&1; \
	$(MAKE) >> ${LOG_FILE} 2>&1 && $(MAKE) install;

x264:
	cd $@; \
	echo -n "$(CURRENT_TIME) building $@ ... " >> $(LOG_FILE); \
	./configure --prefix=$(C_USR_DIR) --extra-cflags="-I$(C_USR_DIR)/include" --extra-ldflags="-L$(C_USR_DIR)/lib" --enable-shared --enable-static --disable-lavf --disable-ffms --disable-opencl >> ${LOG_FILE} 2>&1; \
	$(MAKE) >> ${LOG_FILE} 2>&1 && $(MAKE) install;

sdl:
	cd $(SDL_DIR); \
	echo -n "$(CURRENT_TIME) building $@ ... " >> $(LOG_FILE); \
	./configure --prefix=$(C_USR_DIR) --enable-shared; \
	$(MAKE) && $(MAKE) install;

ffmpeg:
	cd $(FFMPEG_DIR); \
	echo -n "$(CURRENT_TIME) building $@ ... " >> $(LOG_FILE); \
	sed -i -e 's|SDL_CONFIG="$${cross_prefix}sdl-config"|SDL_CONFIG="$(C_USR_DIR)/bin/sdl-config"|' ./configure; \
	./configure --prefix=$(C_USR_DIR) --enable-shared --enable-libfaac --enable-libmp3lame --enable-libx264 --enable-gpl --enable-pthreads --enable-nonfree >> ${LOG_FILE} 2>&1; \
	sed -i -e 's|SDL_CONFIG="$(C_USR_DIR)/bin/sdl-config"|SDL_CONFIG="$${cross_prefix}sdl-config"|' ./configure; \
	$(MAKE) >> ${LOG_FILE} 2>&1 >> ${LOG_FILE} 2>&1 && $(MAKE) install;

clean:
	for dir in $(DIRS); do \
		if [ -e $$dir/Makefile ]; then \
			$(MAKE) --directory=$$dir clean; \
		fi; \
	done
