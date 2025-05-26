#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <jansson.h>
#include <yaml.h>
#include <libxml/parser.h>
#include <libxml/tree.h>

// Data structure to hold key-value pairs
typedef struct {
    char *name;
    int age;
    char *city;
} Person;

// Initialize Person
Person *create_person(const char *name, int age, const char *city) {
    Person *p = malloc(sizeof(Person));
    if (!p) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }
    p->name = name ? strdup(name) : NULL;
    p->age = age;
    p->city = city ? strdup(city) : NULL;
    if ((name && !p->name) || (city && !p->city)) {
        fprintf(stderr, "Memory allocation for strings failed\n");
        free(p->name);
        free(p->city);
        free(p);
        exit(1);
    }
    return p;
}

// Free Person memory
void free_person(Person *p) {
    if (p) {
        free(p->name);
        free(p->city);
        free(p);
    }
}

// Get file extension
const char *get_extension(const char *filename) {
    const char *dot = strrchr(filename, '.');
    if (!dot || dot == filename) return "";
    return dot;
}

// Validate file extension
int is_valid_extension(const char *ext) {
    return strcmp(ext, ".json") == 0 ||
           strcmp(ext, ".yml") == 0 ||
           strcmp(ext, ".yaml") == 0 ||
           strcmp(ext, ".xml") == 0;
}

// Task 2: Read JSON
Person *read_json(const char *filename) {
    json_error_t error;
    json_t *root = json_load_file(filename, 0, &error);
    if (!root) {
        fprintf(stderr, "JSON parsing error: %s (line %d)\n", error.text, error.line);
        return NULL;
    }
    if (!json_is_object(root)) {
        fprintf(stderr, "JSON root is not an object\n");
        json_decref(root);
        return NULL;
    }

    const char *name = json_string_value(json_object_get(root, "name"));
    json_t *age = json_object_get(root, "age");
    const char *city = json_string_value(json_object_get(root, "city"));

    if (!name || !json_is_integer(age) || !city) {
        fprintf(stderr, "Invalid JSON structure\n");
        json_decref(root);
        return NULL;
    }

    Person *p = create_person(name, json_integer_value(age), city);
    json_decref(root);
    return p;
}

// Task 3: Write JSON
int write_json(const Person *p, const char *filename) {
    json_t *root = json_object();
    if (!root) {
        fprintf(stderr, "Failed to create JSON object\n");
        return 1;
    }

    if (json_object_set_new(root, "name", json_string(p->name)) ||
        json_object_set_new(root, "age", json_integer(p->age)) ||
        json_object_set_new(root, "city", json_string(p->city))) {
        fprintf(stderr, "Failed to populate JSON object\n");
        json_decref(root);
        return 1;
    }

    if (json_dump_file(root, filename, JSON_INDENT(2))) {
        fprintf(stderr, "Failed to write JSON to %s\n", filename);
        json_decref(root);
        return 1;
    }

    json_decref(root);
    return 0;
}

// Task 4: Read YAML
Person *read_yaml(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        fprintf(stderr, "Cannot open YAML file %s\n", filename);
        return NULL;
    }

    yaml_parser_t parser;
    if (!yaml_parser_initialize(&parser)) {
        fprintf(stderr, "Failed to initialize YAML parser\n");
        fclose(file);
        return NULL;
    }
    yaml_parser_set_input_file(&parser, file);

    yaml_document_t doc;
    if (!yaml_parser_load(&parser, &doc)) {
        fprintf(stderr, "YAML parsing error\n");
        yaml_parser_delete(&parser);
        fclose(file);
        return NULL;
    }

    yaml_node_t *root = yaml_document_get_root_node(&doc);
    if (!root || root->type != YAML_MAPPING_NODE) {
        fprintf(stderr, "Invalid YAML structure\n");
        yaml_document_delete(&doc);
        yaml_parser_delete(&parser);
        fclose(file);
        return NULL;
    }

    char *name = NULL;
    int age = 0;
    char *city = NULL;

    for (yaml_node_pair_t *pair = root->data.mapping.pairs.start;
         pair < root->data.mapping.pairs.top; pair++) {
        yaml_node_t *key = yaml_document_get_node(&doc, pair->key);
        yaml_node_t *value = yaml_document_get_node(&doc, pair->value);
        if (key->type == YAML_SCALAR_NODE && value->type == YAML_SCALAR_NODE) {
            const char *k = (const char *)key->data.scalar.value;
            const char *v = (const char *)value->data.scalar.value;
            if (strcmp(k, "name") == 0) name = strdup(v);
            else if (strcmp(k, "age") == 0) age = atoi(v);
            else if (strcmp(k, "city") == 0) city = strdup(v);
        }
    }

    if (!name || age <= 0 || !city) {
        fprintf(stderr, "Invalid YAML data\n");
        free(name);
        free(city);
        yaml_document_delete(&doc);
        yaml_parser_delete(&parser);
        fclose(file);
        return NULL;
    }

    Person *p = create_person(name, age, city);
    free(name);
    free(city);
    yaml_document_delete(&doc);
    yaml_parser_delete(&parser);
    fclose(file);
    return p;
}

// Task 5: Write YAML
int write_yaml(const Person *p, const char *filename) {
    FILE *file = fopen(filename, "w");
    if (!file) {
        fprintf(stderr, "Cannot open YAML file %s\n", filename);
        return 1;
    }

    yaml_emitter_t emitter;
    if (!yaml_emitter_initialize(&emitter)) {
        fprintf(stderr, "Failed to initialize YAML emitter\n");
        fclose(file);
        return 1;
    }
    yaml_emitter_set_output_file(&emitter, file);

    yaml_document_t doc;
    yaml_document_initialize(&doc, NULL, NULL, NULL, 1, 1);

    yaml_node_t *root = yaml_document_add_mapping(&doc, NULL, YAML_BLOCK_MAPPING_STYLE);
    yaml_document_append_mapping_pair(&doc, root->id,
        yaml_document_add_scalar(&doc, NULL, (yaml_char_t *)"name", -1, YAML_PLAIN_SCALAR_STYLE),
        yaml_document_add_scalar(&doc, NULL, (yaml_char_t *)p->name, -1, YAML_PLAIN_SCALAR_STYLE));
    char age_str[16];
    snprintf(age_str, sizeof(age_str), "%d", p->age);
    yaml_document_append_mapping_pair(&doc, root->id,
        yaml_document_add_scalar(&doc, NULL, (yaml_char_t *)"age", -1, YAML_PLAIN_SCALAR_STYLE),
        yaml_document_add_scalar(&doc, NULL, (yaml_char_t *)age_str, -1, YAML_PLAIN_SCALAR_STYLE));
    yaml_document_append_mapping_pair(&doc, root->id,
        yaml_document_add_scalar(&doc, NULL, (yaml_char_t *)"city", -1, YAML_PLAIN_SCALAR_STYLE),
        yaml_document_add_scalar(&doc, NULL, (yaml_char_t *)p->city, -1, YAML_PLAIN_SCALAR_STYLE));

    if (!yaml_emitter_dump(&emitter, &doc)) {
        fprintf(stderr, "Failed to write YAML to %s\n", filename);
        yaml_emitter_delete(&emitter);
        yaml_document_delete(&doc);
        fclose(file);
        return 1;
    }

    yaml_emitter_delete(&emitter);
    yaml_document_delete(&doc);
    fclose(file);
    return 0;
}

// Task 6: Read XML
Person *read_xml(const char *filename) {
    xmlDoc *doc = xmlReadFile(filename, NULL, 0);
    if (!doc) {
        fprintf(stderr, "Failed to parse XML file %s\n", filename);
        return NULL;
    }

    xmlNode *root = xmlDocGetRootElement(doc);
    if (!root || strcmp((const char *)root->name, "person") != 0) {
        fprintf(stderr, "Invalid XML root element\n");
        xmlFreeDoc(doc);
        return NULL;
    }

    char *name = NULL;
    int age = 0;
    char *city = NULL;

    for (xmlNode *node = root->children; node; node = node->next) {
        if (node->type == XML_ELEMENT_NODE) {
            xmlChar *content = xmlNodeGetContent(node);
            if (!content) continue;
            if (strcmp((const char *)node->name, "name") == 0) name = strdup((const char *)content);
            else if (strcmp((const char *)node->name, "age") == 0) age = atoi((const char *)content);
            else if (strcmp((const char *)node->name, "city") == 0) city = strdup((const char *)content);
            xmlFree(content);
        }
    }

    if (!name || age <= 0 || !city) {
        fprintf(stderr, "Invalid XML data\n");
        free(name);
        free(city);
        xmlFreeDoc(doc);
        return NULL;
    }

    Person *p = create_person(name, age, city);
    free(name);
    free(city);
    xmlFreeDoc(doc);
    return p;
}

// Task 7: Write XML
int write_xml(const Person *p, const char *filename) {
    xmlDoc *doc = xmlNewDoc(BAD_CAST "1.0");
    xmlNode *root = xmlNewNode(NULL, BAD_CAST "person");
    xmlDocSetRootElement(doc, root);

    xmlNewChild(root, NULL, BAD_CAST "name", BAD_CAST p->name);
    char age_str[16];
    snprintf(age_str, sizeof(age_str), "%d", p->age);
    xmlNewChild(root, NULL, BAD_CAST "age", BAD_CAST age_str);
    xmlNewChild(root, NULL, BAD_CAST "city", BAD_CAST p->city);

    if (xmlSaveFormatFileEnc(filename, doc, "UTF-8", 1) == -1) {
        fprintf(stderr, "Failed to write XML to %s\n", filename);
        xmlFreeDoc(doc);
        return 1;
    }

    xmlFreeDoc(doc);
    return 0;
}

// Task 1: Parse arguments and dispatch
int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s pathFile1.x pathFile2.y\n", argv[0]);
        fprintf(stderr, "Extensions: .json, .yml, .yaml, .xml\n");
        fprintf(stderr, "Example: %s input.json output.yaml\n", argv[0]);
        return 1;
    }

    const char *input_file = argv[1];
    const char *output_file = argv[2];
    const char *input_ext = get_extension(input_file);
    const char *output_ext = get_extension(output_file);

    if (!is_valid_extension(input_ext) || !is_valid_extension(output_ext)) {
        fprintf(stderr, "Invalid file extension. Use .json, .yml, .yaml, or .xml\n");
        return 1;
    }

    // Read input file
    Person *p = NULL;
    if (strcmp(input_ext, ".json") == 0) {
        p = read_json(input_file);
    } else if (strcmp(input_ext, ".yml") == 0 || strcmp(input_ext, ".yaml") == 0) {
        p = read_yaml(input_file);
    } else if (strcmp(input_ext, ".xml") == 0) {
        p = read_xml(input_file);
    }

    if (!p) {
        fprintf(stderr, "Failed to read input file %s\n", input_file);
        return 1;
    }

    // Write output file
    int result = 1;
    if (strcmp(output_ext, ".json") == 0) {
        result = write_json(p, output_file);
    } else if (strcmp(output_ext, ".yml") == 0 || strcmp(output_ext, ".yaml") == 0) {
        result = write_yaml(p, output_file);
    } else if (strcmp(output_ext, ".xml") == 0) {
        result = write_xml(p, output_file);
    }

    free_person(p);
    if (result) {
        fprintf(stderr, "Failed to write output file %s\n", output_file);
        return 1;
    }

    printf("Successfully converted %s to %s\n", input_file, output_file);
    return 0;
}
