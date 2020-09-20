from argparse import ArgumentParser
from mdiocre.wizard import Wizard
from mdiocre.utils import Logger

APP_NAME    = 'MDiocre'
APP_VERSION = '3.2a'
APP_DATE    = '2020-09-15'

if __name__ == '__main__':
	ap = ArgumentParser(
			description='A terrible static page generator.'
		)

	ap.add_argument('source_dir', help='Webpages source directory')
	ap.add_argument('build_dir', help='Output directory')
	ap.add_argument('--quiet', '-q', help='No output', action='store_true')

	args = ap.parse_args()

	w = Wizard(quiet=args.quiet)

	# display header
	if not args.quiet:
		print()
		app_str = "{} version {} ({})".format(APP_NAME, APP_VERSION, APP_DATE)
		print(app_str)
		print('='*len(app_str))
		print()

	# run the wizard
	w.generate_from_directory(vars(args))
