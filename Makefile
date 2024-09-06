docs_preview:
	echo "Previewing docs..."
	mkdocs serve

docs_deploy:
	echo "Building docs..."
	mkdocs gh-deploy --force
